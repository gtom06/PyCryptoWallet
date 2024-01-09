from portfolio import Portfolio

def main():
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

if __name__ == "__main__":
    main()
