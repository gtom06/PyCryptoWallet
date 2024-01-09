import json
from datetime import datetime, timedelta, timezone
import requests
import logging

PORTFOLIO_FILE = '../data/portfolio.json'
COINS_LIST_FILE = '../data/cryptocoinslist.json'
LOGGING_INTERVAL_DAYS = 7

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
print('hello te')

class Portfolio:
    REQ_PRICE = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=eur&include_market_cap=false&include_24hr_vol=false&include_24hr_change=false&include_last_updated_at=false&precision=full"
    REQ_COINS_LIST = 'https://api.coingecko.com/api/v3/coins/list'

    def __init__(self, portfolio_filename=PORTFOLIO_FILE, coinslist_filename=COINS_LIST_FILE,
                 update_interval_days=LOGGING_INTERVAL_DAYS):
        self.portfolio_filename = portfolio_filename
        self.coinslist_filename = coinslist_filename
        self.update_interval_days = update_interval_days
        self.cryptos_owned = JsonFileManager.load_json(self.portfolio_filename, {}).get("cryptos_owned", {})
        self.coins_list_data = JsonFileManager.load_json(self.coinslist_filename,
                                                         {"supported_coins": [], "last_requested_date": None})

    def update_portfolio(self):
        JsonFileManager.save_json(self.portfolio_filename, {"cryptos_owned": self.cryptos_owned})

    def update_coins_list(self, req_coins_list):
        try:
            response = ApiRequestManager.get(req_coins_list)
            response.raise_for_status()
            coins_list = response.json()

            if not isinstance(coins_list, list):
                raise ValueError("Invalid coins list format")

            coins_data = {
                "last_requested_date": datetime.now(timezone.utc).isoformat(),
                "supported_coins": coins_list
            }

            JsonFileManager.save_json(self.coinslist_filename, coins_data)

            return coins_list, coins_data["last_requested_date"]
        except requests.RequestException as e:
            logger.error(f"Error updating coins list: {e}")
            return None, None

    def should_update_coins_list(self):
        return JsonFileManager.should_update_coins_list(self.coins_list_data, self.update_interval_days)

    def get_coin_id(self, symbol):
        for coin_data in self.coins_list_data["supported_coins"]:
            if isinstance(coin_data, dict) and "symbol" in coin_data and coin_data["symbol"] == symbol:
                return coin_data["id"]
        return None

    def add_crypto(self, crypto_symbol, crypto_amount, amount_euro_spent):
        self.update_supported_coins_list()
        coin_id = self.get_coin_id(crypto_symbol)
        if coin_id is not None:
            qty_before = self.cryptos_owned.get(crypto_symbol, {}).get("qty", 0)
            amount_before = self.cryptos_owned.get(crypto_symbol, {}).get("amount_euro_spent", 0)

            self.cryptos_owned[crypto_symbol] = {
                "coin_id": coin_id,
                "qty": qty_before + crypto_amount,
                "amount_euro_spent": amount_before + amount_euro_spent,
                "last_modified_date": datetime.now(timezone.utc).isoformat()
            }

            if qty_before != self.cryptos_owned[crypto_symbol]["qty"] or amount_before != \
                    self.cryptos_owned[crypto_symbol]["amount_euro_spent"]:
                self.update_portfolio()
        else:
            logger.warning(f"Coin with symbol {crypto_symbol} not found in coins list.")

    def display_portfolio(self):
        for crypto_symbol, crypto_data in self.cryptos_owned.items():
            qty = crypto_data.get('qty', 0)
            amount_euro_spent = crypto_data.get('amount_euro_spent', 0)

            if qty != 0:
                price_per_coin = amount_euro_spent / qty
            else:
                price_per_coin = 0

            print(f"{crypto_symbol}: {qty} "
                  f"(Amount Euro Spent: {amount_euro_spent}, "
                  f"priceXcoin: {price_per_coin})")

    def update_supported_coins_list(self):
        if self.should_update_coins_list():
            updated_coins_list, last_requested_date = self.update_coins_list(self.REQ_COINS_LIST)
            if updated_coins_list:
                self.coins_list_data = {"supported_coins": updated_coins_list,
                                        "last_requested_date": last_requested_date}

    def get_portfolio_prices(self):
        coin_ids = self.get_portfolio_ids()
        param = "%2C".join(coin_ids)
        request_url = Portfolio.REQ_PRICE.format(param)
        response = ApiRequestManager.get(request_url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error fetching portfolio prices. Status code: {response.status_code}")
            return None

    def get_portfolio_ids(self):
        return [crypto_data.get('coin_id', '') for crypto_data in self.cryptos_owned.values() if
                'coin_id' in crypto_data]

    def get_actual_values(self):
        prices = self.get_portfolio_prices()
        if prices:
            return {symbol: data['eur'] for symbol, data in prices.items()}
        else:
            return {}

    def calculate_portfolio_values(self):
        actual_values = self.get_actual_values()
        if not actual_values:
            return {}

        portfolio_values = {}
        for symbol, crypto_data in self.cryptos_owned.items():
            qty = crypto_data.get('qty', 0)
            coin_id = crypto_data.get('coin_id', '')
            actual_value = actual_values.get(coin_id, 0)

            value_in_euro = qty * actual_value
            portfolio_values[symbol] = value_in_euro

        return portfolio_values

class JsonFileManager:
    @staticmethod
    def load_json(filename, default_value):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            JsonFileManager.save_json(filename, default_value)
            return default_value

    @staticmethod
    def save_json(filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def should_update_coins_list(coins_list_data, update_interval_days):
        last_requested_date = coins_list_data.get("last_requested_date")

        if not last_requested_date or not isinstance(last_requested_date, str):
            return True

        try:
            last_requested_date = datetime.fromisoformat(last_requested_date)
            update_threshold = datetime.now(timezone.utc) - timedelta(days=update_interval_days)
            return last_requested_date < update_threshold
        except ValueError:
            return True

class ApiRequestManager:
    @staticmethod
    def get(url):
        return requests.get(url)

crypto_symbol = "BTC"
crypto_amount = 1.5
amount_euro_spent = 50000

portfolio = Portfolio()
portfolio.add_crypto(crypto_symbol, crypto_amount, amount_euro_spent)
portfolio.display_portfolio()

actual_values = portfolio.get_actual_values()
print(actual_values)

portfolio_values = portfolio.calculate_portfolio_values()
print(portfolio_values)
