import threading
import time

from portfolio import Portfolio

def main():
    #crypto_symbol = "BTC"
    #crypto_amount = 1.5
    #amount_euro_spent = 50000

    portfolio = Portfolio()
    #portfolio.add_crypto(crypto_symbol, crypto_amount, amount_euro_spent)
    #portfolio.display_portfolio()

    #actual_values = portfolio.get_actual_values()
    #print(actual_values)


    #print(portfolio.calculate_portfolio_values_2())
    portfolio.calculate_and_save_portfolio_values()
    #portfolio2 = Portfolio("", "","")

if __name__ == "__main__":
    while(1):
        thread = threading.Thread(target=main)
        thread.start()
        thread.join()
        time.sleep(120)
