import threading
import time

from portfolio import Portfolio

def main():
    portfolio = Portfolio()
    portfolio.calculate_and_save_portfolio_values()


if __name__ == "__main__":
    while(1):
        thread = threading.Thread(target=main)
        thread.start()
        thread.join()
        time.sleep(120)
