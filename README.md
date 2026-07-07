# Investment Tracker

A simple command-line tool for tracking your stock investments — ticker symbols, share counts, and purchase prices — saved locally in a JSON file.

## Features

- Add new investments (ticker, shares, purchase price)
- View all tracked investments with cost basis calculated automatically
- Data persists between runs in a local `investments.json` file
- No external dependencies — pure Python standard library

## Requirements

- Python 3.7+

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/csegna/investment-tracker.git
cd investment-tracker
```

No dependencies to install — the script only uses Python's standard library.

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
3. Quit
```

- **1** — Add an investment by entering a ticker symbol, number of shares, and purchase price per share.
- **2** — View all investments you've added, including cost basis (shares × purchase price) for each.
- **3** — Quit the program.

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

- Live price lookups and unrealized gain/loss calculation
- Editing and deleting existing entries
- Averaging cost basis across multiple buys of the same ticker
- Sell transactions with realized gain/loss tracking
- CSV export

## License

MIT — see [LICENSE](LICENSE) for details.
