import threading
import time

from portfolio import Portfolio


if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.add_crypto("BTC", 2, 200)  # Esempio di add_crypto
    portfolio.display_portfolio()
