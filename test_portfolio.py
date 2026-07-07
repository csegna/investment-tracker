"""Tests for portfolio.py.

Run with: pytest

These functions are pure (no input(), no print(), no file access), so each
test just calls a function with known numbers and checks the math - no
network, no mocking, no setup required.
"""

from portfolio import (
    add_allocation_percentages,
    calculate_portfolio_totals,
    calculate_position,
)


# --- calculate_position ---

def test_calculate_position_with_a_gain():
    investment = {"ticker": "AAPL", "shares": 10.0, "purchase_price": 100.0}

    position = calculate_position(investment, current_price=150.0)

    assert position["cost_basis"] == 1000.0
    assert position["current_value"] == 1500.0
    assert position["gain_loss_dollars"] == 500.0
    assert position["gain_loss_percent"] == 50.0


def test_calculate_position_with_a_loss():
    investment = {"ticker": "RR", "shares": 12.0, "purchase_price": 3.78}

    position = calculate_position(investment, current_price=1.91)

    assert round(position["cost_basis"], 2) == 45.36
    assert round(position["current_value"], 2) == 22.92
    assert round(position["gain_loss_dollars"], 2) == -22.44
    assert position["gain_loss_percent"] < 0


def test_calculate_position_with_no_change():
    investment = {"ticker": "MSFT", "shares": 5.0, "purchase_price": 300.0}

    position = calculate_position(investment, current_price=300.0)

    assert position["gain_loss_dollars"] == 0.0
    assert position["gain_loss_percent"] == 0.0


def test_calculate_position_handles_zero_cost_basis():
    # purchase_price of 0 would normally cause a divide-by-zero when
    # computing gain_loss_percent - it should return 0.0 instead of crashing.
    investment = {"ticker": "FREE", "shares": 10.0, "purchase_price": 0.0}

    position = calculate_position(investment, current_price=5.0)

    assert position["cost_basis"] == 0.0
    assert position["gain_loss_percent"] == 0.0


def test_calculate_position_keeps_ticker_and_inputs():
    investment = {"ticker": "TSLA", "shares": 3.0, "purchase_price": 200.0}

    position = calculate_position(investment, current_price=250.0)

    assert position["ticker"] == "TSLA"
    assert position["shares"] == 3.0
    assert position["purchase_price"] == 200.0
    assert position["current_price"] == 250.0


# --- calculate_portfolio_totals ---

def test_calculate_portfolio_totals_sums_multiple_positions():
    positions = [
        {"cost_basis": 1000.0, "current_value": 1500.0},
        {"cost_basis": 45.36, "current_value": 22.92},
    ]

    totals = calculate_portfolio_totals(positions)

    assert round(totals["total_cost_basis"], 2) == 1045.36
    assert round(totals["total_value"], 2) == 1522.92
    assert round(totals["total_gain_loss"], 2) == 477.56


def test_calculate_portfolio_totals_with_no_positions():
    totals = calculate_portfolio_totals([])

    assert totals["total_cost_basis"] == 0
    assert totals["total_value"] == 0
    assert totals["total_gain_loss"] == 0


# --- add_allocation_percentages ---

def test_add_allocation_percentages_splits_evenly():
    positions = [
        {"ticker": "A", "current_value": 500.0},
        {"ticker": "B", "current_value": 500.0},
    ]

    add_allocation_percentages(positions, total_value=1000.0)

    assert positions[0]["allocation_percent"] == 50.0
    assert positions[1]["allocation_percent"] == 50.0


def test_add_allocation_percentages_handles_uneven_split():
    positions = [
        {"ticker": "A", "current_value": 750.0},
        {"ticker": "B", "current_value": 250.0},
    ]

    add_allocation_percentages(positions, total_value=1000.0)

    assert positions[0]["allocation_percent"] == 75.0
    assert positions[1]["allocation_percent"] == 25.0


def test_add_allocation_percentages_handles_zero_total_value():
    # If every position is worthless, dividing by total_value would
    # normally crash - it should return 0.0 for each instead.
    positions = [{"ticker": "A", "current_value": 0.0}]

    add_allocation_percentages(positions, total_value=0.0)

    assert positions[0]["allocation_percent"] == 0.0
