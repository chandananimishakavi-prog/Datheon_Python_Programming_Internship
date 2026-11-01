import csv
import os
from datetime import datetime
import yfinance as yf
portfolio = {}
def get_current_price(symbol):
    try:
        # Yahoo Finance uses BRK-B instead of BRK.B
        yahoo_symbol = symbol.replace(".", "-")

        stock = yf.Ticker(yahoo_symbol)

        price = stock.fast_info.get("lastPrice")

        if price is None:
            history = stock.history(period="5d")
            if history.empty:
                return None
            price = history["Close"].dropna().iloc[-1]

        return float(price)

    except Exception:
        return None
def add_stock():
    symbol = input("Enter stock ticker symbol: ").upper()

    try:
        buy_price = float(input("Enter purchase price: "))
        quantity = int(input("Enter number of shares: "))

        if buy_price <= 0 or quantity <= 0:
            print("Price and quantity must be positive.")
            return

        portfolio[symbol] = {
            "buy_price": buy_price,
            "quantity": quantity
        }

        print("Stock added successfully!")

    except ValueError:
        print("Please enter valid numeric values.")


# Function to calculate portfolio performance
def calculate_portfolio():
    total_investment = 0
    total_value = 0
    results = []

    print("\n========== PORTFOLIO SUMMARY ==========")

    for symbol, details in portfolio.items():

        buy_price = details["buy_price"]
        quantity = details["quantity"]

        current_price = get_current_price(symbol)

        if current_price is None:
            print(f"Unable to fetch price for {symbol}")
            continue

        invested = buy_price * quantity
        market_value = current_price * quantity

        profit_loss = market_value - invested

        percentage = (profit_loss / invested) * 100

        total_investment += invested
        total_value += market_value

        print(f"\nStock: {symbol}")
        print(f"Purchase Price: ${buy_price:.2f}")
        print(f"Current Price: ${current_price:.2f}")
        print(f"Quantity: {quantity}")
        print(f"Invested Amount: ${invested:.2f}")
        print(f"Current Value: ${market_value:.2f}")
        print(f"Profit/Loss: ${profit_loss:.2f}")
        print(f"Percentage Gain/Loss: {percentage:.2f}%")

        results.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Symbol": symbol,
            "Buy Price": buy_price,
            "Current Price": current_price,
            "Quantity": quantity,
            "Invested Amount": invested,
            "Current Value": market_value,
            "Profit/Loss": profit_loss,
            "Percentage": percentage
        })

    if total_investment > 0:

        total_profit = total_value - total_investment

        total_percentage = (
            total_profit / total_investment
        ) * 100

        print("\n========== TOTAL PORTFOLIO ==========")
        print(f"Total Investment: ${total_investment:.2f}")
        print(f"Total Market Value: ${total_value:.2f}")
        print(f"Total Profit/Loss: ${total_profit:.2f}")
        print(f"Overall Return: {total_percentage:.2f}%")

        save_to_csv(results)


# Function to save results into CSV
def save_to_csv(results):

    filename = "portfolio_summary.csv"

    if not results:
        return

    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        if not file_exists or os.path.getsize(filename) == 0:
            writer.writeheader()

        writer.writerows(results)

    print("\nPortfolio summary saved successfully!")


# Main menu
def main():

    while True:

        print("\n===== STOCK PORTFOLIO TRACKER =====")
        print("1. Add Stock")
        print("2. View Portfolio Performance")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_stock()

        elif choice == "2":
            if portfolio:
                calculate_portfolio()
            else:
                print("Portfolio is empty. Add stocks first.")

        elif choice == "3":
            print("Thank you for using Stock Portfolio Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
