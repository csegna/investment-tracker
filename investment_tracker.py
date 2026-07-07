import json
import os

import pricing
import portfolio

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


def view_portfolio_performance(investments):
    if not investments:
        print("No investments tracked yet.")
        return

    print("\nFetching current prices...")
    positions = []
    for inv in investments:
        price = pricing.get_current_price(inv["ticker"])
        if price is None:
            print(f"Could not fetch a price for {inv['ticker']} - skipping it.")
            continue
        positions.append(portfolio.calculate_position(inv, price))

    if not positions:
        print("Couldn't fetch any prices. Check your internet connection and try again.\n")
        return

    totals = portfolio.calculate_portfolio_totals(positions)
    portfolio.add_allocation_percentages(positions, totals["total_value"])

    print("\nPortfolio performance:")
    for p in positions:
        print(
            f"\n{p['ticker']} - {p['shares']} shares @ current price ${p['current_price']:.2f}"
        )
        print(f"  Cost basis:     ${p['cost_basis']:.2f}")
        print(f"  Current value:  ${p['current_value']:.2f}")
        print(f"  Gain/Loss:      ${p['gain_loss_dollars']:.2f} ({p['gain_loss_percent']:.2f}%)")
        print(f"  Allocation:     {p['allocation_percent']:.2f}% of portfolio")

    print("\nPortfolio totals:")
    print(f"  Total cost basis:    ${totals['total_cost_basis']:.2f}")
    print(f"  Total current value: ${totals['total_value']:.2f}")
    print(f"  Total gain/loss:     ${totals['total_gain_loss']:.2f}")
    print()


def main():
    investments = load_investments()

    while True:
        print("What would you like to do?")
        print("1. Add an investment")
        print("2. View investments")
        print("3. View portfolio performance (live prices)")
        print("4. Quit")
        choice = input("Enter 1, 2, 3, or 4: ")

        if choice == "1":
            add_investment(investments)
        elif choice == "2":
            list_investments(investments)
        elif choice == "3":
            view_portfolio_performance(investments)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main()
