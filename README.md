# Investment Tracker

[![Tests](https://github.com/csegna/investment-tracker/actions/workflows/tests.yml/badge.svg)](https://github.com/csegna/investment-tracker/actions/workflows/tests.yml)

A simple command-line tool for tracking your stock investments — ticker symbols, share counts, and purchase prices — saved locally in a JSON file.

## Features

- Add new investments (ticker, shares, purchase price)
- View all tracked investments with cost basis calculated automatically
- Live portfolio performance using real market prices (via [yfinance](https://pypi.org/project/yfinance/)):
  - Current price and current value per holding
  - Unrealized gain/loss in dollars and percent, per holding
  - Portfolio-wide totals: cost basis, current value, gain/loss
  - Allocation percentage per holding
- Data persists between runs in a local `investments.json` file
- A Streamlit dashboard (`dashboard.py`) with the same data as a visual view: headline stats, a positions table, an allocation pie chart, and a gain/loss bar chart

## Requirements

- Python 3.7+
- `yfinance` (for live price lookups — see Installation below)
- `streamlit`, `plotly`, `pandas` (for the dashboard only — see Installation below)

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/csegna/investment-tracker.git
cd investment-tracker
```

Install the one required package:

```bash
pip3 install -r requirements.txt
```

## Usage

Run the script:

```bash
python3 investment_tracker.py
```

You'll see a menu:

```
What would you like to do?
1. Add an investment
2. View investments
3. View portfolio performance (live prices)
4. Quit
```

- **1** — Add an investment by entering a ticker symbol, number of shares, and purchase price per share.
- **2** — View all investments you've added, including cost basis (shares × purchase price) for each. Works offline, no live data.
- **3** — Fetch current market prices and show full performance: current value, gain/loss ($ and %), allocation %, and portfolio totals. Requires an internet connection.
- **4** — Quit.

## Dashboard

For a visual view of the same data, run:

```bash
streamlit run dashboard.py
```

This opens a browser tab showing:
- Total portfolio value and total gain/loss as headline stats
- A table of all positions (cost basis, current value, gain/loss, allocation)
- A pie chart of allocation by holding
- A bar chart of gain/loss by holding (green = gain, red = loss)

It reads the same `investments.json` and fetches the same live prices as the CLI's option 3 — it's just a different view, not separate data. Refresh the page to re-fetch current prices.

## Testing

The calculation logic in `portfolio.py` has a pytest suite in `test_portfolio.py`. Install the dev dependencies (this includes everything in `requirements.txt`, plus `pytest`):

```bash
pip3 install -r requirements-dev.txt
```

Run the tests:

```bash
pytest
```

These tests only exercise `portfolio.py` — they don't hit the network or yfinance, so they run instantly and don't need an internet connection.

## Data storage

Your investments are stored in `investments.json`, created automatically in the same directory as the script the first time you add an investment. This file is excluded from version control (see `.gitignore`) since it contains your personal financial data.

An `investments.example.json` file is included to show the expected format:

```json
[
  {
    "ticker": "AAPL",
    "shares": 10.0,
    "purchase_price": 150.25
  }
]
```

Writes are atomic (via a temp file + rename), so an interrupted save won't corrupt your data. If `investments.json` ever becomes corrupted or unreadable, the program will warn you and start fresh rather than crashing.

## Roadmap

Planned improvements:

- Editing and deleting existing entries
- Averaging cost basis across multiple buys of the same ticker
- Sell transactions with realized gain/loss tracking
- CSV export

## License

MIT — see [LICENSE](LICENSE) for details.
