"""Streamlit dashboard for the investment tracker.

Run with: streamlit run dashboard.py

Reuses the same investments.json, pricing.py, and portfolio.py that the
CLI (investment_tracker.py) uses - this is just a different view on the
same data, not a separate app.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import pricing
import portfolio
from investment_tracker import load_investments

# Colors: categorical slots for "which holding", status colors for "good/bad".
# See project docs (dataviz skill) for why these two are kept separate.
CATEGORICAL_COLORS = [
    "#2a78d6", "#1baf7a", "#eda100", "#008300",
    "#4a3aa7", "#e34948", "#e87ba4", "#eb6834",
]
OTHER_COLOR = "#898781"
GOOD_COLOR = "#0ca30c"
CRITICAL_COLOR = "#d03b3b"
BASELINE_COLOR = "#c3c2b7"

MAX_PIE_SLICES = 8

st.set_page_config(page_title="Investment Tracker Dashboard", layout="wide")
st.title("Investment Tracker Dashboard")

investments = load_investments()

if not investments:
    st.info(
        "No investments tracked yet. Add some with the CLI "
        "(`python3 investment_tracker.py`), then refresh this page."
    )
    st.stop()

with st.spinner("Fetching current prices..."):
    positions = []
    for inv in investments:
        price = pricing.get_current_price(inv["ticker"])
        if price is None:
            st.warning(f"Could not fetch a price for {inv['ticker']} - skipping it.")
            continue
        positions.append(portfolio.calculate_position(inv, price))

if not positions:
    st.error("Couldn't fetch any prices. Check your internet connection and try again.")
    st.stop()

totals = portfolio.calculate_portfolio_totals(positions)
portfolio.add_allocation_percentages(positions, totals["total_value"])

df = pd.DataFrame(positions)

# --- Headline numbers ---
col1, col2 = st.columns(2)
col1.metric("Total Portfolio Value", f"${totals['total_value']:,.2f}")

gain_loss = totals["total_gain_loss"]
cost_basis = totals["total_cost_basis"]
gain_loss_pct = (gain_loss / cost_basis * 100) if cost_basis else 0.0
col2.metric("Total Gain/Loss", f"${gain_loss:,.2f}", f"{gain_loss_pct:.2f}%")

# --- Positions table ---
st.subheader("Positions")
table = df.rename(columns={
    "ticker": "Ticker",
    "shares": "Shares",
    "purchase_price": "Purchase Price",
    "current_price": "Current Price",
    "cost_basis": "Cost Basis",
    "current_value": "Current Value",
    "gain_loss_dollars": "Gain/Loss ($)",
    "gain_loss_percent": "Gain/Loss (%)",
    "allocation_percent": "Allocation (%)",
})
column_order = [
    "Ticker", "Shares", "Purchase Price", "Current Price", "Cost Basis",
    "Current Value", "Gain/Loss ($)", "Gain/Loss (%)", "Allocation (%)",
]
st.dataframe(
    table[column_order].style.format({
        "Shares": "{:.2f}",
        "Purchase Price": "${:.2f}",
        "Current Price": "${:.2f}",
        "Cost Basis": "${:.2f}",
        "Current Value": "${:.2f}",
        "Gain/Loss ($)": "${:.2f}",
        "Gain/Loss (%)": "{:.2f}%",
        "Allocation (%)": "{:.2f}%",
    }),
    use_container_width=True,
    hide_index=True,
)

# --- Allocation pie chart ---
st.subheader("Allocation by Holding")

by_value = df.sort_values("current_value", ascending=False).reset_index(drop=True)
if len(by_value) > MAX_PIE_SLICES:
    # Fold the smallest holdings into "Other" instead of adding a 9th
    # generated color - past 8 slots colors stop being distinguishable.
    top = by_value.iloc[: MAX_PIE_SLICES - 1]
    other_total = by_value.iloc[MAX_PIE_SLICES - 1:]["current_value"].sum()
    other_row = pd.DataFrame([{"ticker": "Other", "current_value": other_total}])
    pie_data = pd.concat([top[["ticker", "current_value"]], other_row], ignore_index=True)
    pie_colors = CATEGORICAL_COLORS[: MAX_PIE_SLICES - 1] + [OTHER_COLOR]
else:
    pie_data = by_value[["ticker", "current_value"]]
    pie_colors = CATEGORICAL_COLORS[: len(pie_data)]

fig_pie = px.pie(
    pie_data,
    names="ticker",
    values="current_value",
    color="ticker",
    color_discrete_sequence=pie_colors,
)
fig_pie.update_traces(textinfo="label+percent", textposition="outside")
st.plotly_chart(fig_pie, use_container_width=True)

# --- Gain/loss by holding ---
st.subheader("Gain/Loss by Holding")

by_gain_loss = df.sort_values("gain_loss_dollars")
bar_colors = [GOOD_COLOR if v >= 0 else CRITICAL_COLOR for v in by_gain_loss["gain_loss_dollars"]]

fig_bar = go.Figure(go.Bar(
    x=by_gain_loss["gain_loss_dollars"],
    y=by_gain_loss["ticker"],
    orientation="h",
    marker_color=bar_colors,
))
fig_bar.update_layout(xaxis_title="Gain / Loss ($)", yaxis_title=None, showlegend=False)
fig_bar.add_vline(x=0, line_width=1, line_color=BASELINE_COLOR)
st.plotly_chart(fig_bar, use_container_width=True)
