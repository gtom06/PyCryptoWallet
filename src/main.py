import threading
import time
import sys

from portfolio import Portfolio

def main_loop(portfolio):
    try:
        while True:
            portfolio.calculate_and_save_portfolio_values()
            time.sleep(120)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting...")
        sys.exit()

def perform_operations(portfolio):
    while True:
        try:
            # Esegui operazioni come add_crypto qui nel thread principale
            crypto_symbol = input("Enter the cryptocurrency symbol: ")
            quantity = float(input("Enter the quantity: "))
            price = float(input("Enter the price: "))

            # Esempio di add_crypto con i parametri inseriti dall'utente
            portfolio.add_crypto(crypto_symbol, quantity, price)
            time.sleep(10)  # Esempio: attendi 10 secondi prima di eseguire la prossima operazione

        except ValueError as e:
            print(f"Error: {e}. Please enter valid numeric values for quantity and price.")
            # You can choose to handle this error in a way that makes sense for your application.

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Handle other unexpected errors here.

if __name__ == "__main__":
    portfolio = Portfolio()

    # Crea un thread per main_loop
    main_thread = threading.Thread(target=main_loop, args=(portfolio,))
    main_thread.start()

    # Esegui perform_operations nel thread principale
    perform_operations(portfolio)
