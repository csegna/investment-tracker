"""Pure calculation functions for portfolio performance.

Nothing in this file reads input(), prints, or touches files -
that keeps it easy to test and reuse.
"""


def calculate_position(investment, current_price):
    """Work out cost basis, current value, and gain/loss for one holding."""
    shares = investment["shares"]
    purchase_price = investment["purchase_price"]

    cost_basis = shares * purchase_price
    current_value = shares * current_price
    gain_loss_dollars = current_value - cost_basis
    gain_loss_percent = (gain_loss_dollars / cost_basis * 100) if cost_basis else 0.0

    return {
        "ticker": investment["ticker"],
        "shares": shares,
        "purchase_price": purchase_price,
        "current_price": current_price,
        "cost_basis": cost_basis,
        "current_value": current_value,
        "gain_loss_dollars": gain_loss_dollars,
        "gain_loss_percent": gain_loss_percent,
    }


def calculate_portfolio_totals(positions):
    """Add up cost basis, current value, and gain/loss across all positions."""
    total_cost_basis = sum(p["cost_basis"] for p in positions)
    total_value = sum(p["current_value"] for p in positions)
    total_gain_loss = total_value - total_cost_basis

    return {
        "total_cost_basis": total_cost_basis,
        "total_value": total_value,
        "total_gain_loss": total_gain_loss,
    }


def add_allocation_percentages(positions, total_value):
    """Add an 'allocation_percent' field to each position, in place."""
    for position in positions:
        if total_value:
            position["allocation_percent"] = position["current_value"] / total_value * 100
        else:
            position["allocation_percent"] = 0.0
    return positions
