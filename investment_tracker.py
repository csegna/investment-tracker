import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "investments.json")


def load_investments():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} is corrupted. Starting with an empty list.")
        return []


def save_investments(investments):
    tmp_file = DATA_FILE + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(investments, f, indent=2)
    os.replace(tmp_file, DATA_FILE)


def add_investment(investments):
    ticker = input("Enter ticker symbol (e.g. AAPL): ").upper()
    shares = float(input("Enter number of shares: "))
    purchase_price = float(input("Enter purchase price per share: $"))

    investment = {
        "ticker": ticker,
        "shares": shares,
        "purchase_price": purchase_price,
    }
    investments.append(investment)
    save_investments(investments)
    print(f"Added {shares} shares of {ticker} at ${purchase_price:.2f} each.")


def list_investments(investments):
    if not investments:
        print("No investments tracked yet.")
        return

    print("\nYour investments:")
    for i, inv in enumerate(investments, start=1):
        cost = inv["shares"] * inv["purchase_price"]
        print(
            f"{i}. {inv['ticker']} - {inv['shares']} shares @ "
            f"${inv['purchase_price']:.2f} (cost basis: ${cost:.2f})"
        )
    print()


def main():
    investments = load_investments()

    while True:
        print("What would you like to do?")
        print("1. Add an investment")
        print("2. View investments")
        print("3. Quit")
        choice = input("Enter 1, 2, or 3: ")

        if choice == "1":
            add_investment(investments)
        elif choice == "2":
            list_investments(investments)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main()
