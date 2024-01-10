import threading
import time

from portfolio import Portfolio

def main_loop(portfolio):
    while True:
        portfolio.calculate_and_save_portfolio_values()
        time.sleep(120)

def perform_operations(portfolio):
    while True:
        # Esegui operazioni come add_crypto qui nel thread principale
        portfolio.add_crypto("btc", 2, 200)  # Esempio di add_crypto
        time.sleep(10)  # Esempio: attendi 10 secondi prima di eseguire la prossima operazione

if __name__ == "__main__":
    portfolio = Portfolio()

    # Crea un thread per main_loop
    main_thread = threading.Thread(target=main_loop, args=(portfolio,))
    main_thread.start()

    # Esegui perform_operations nel thread principale
    perform_operations(portfolio)
