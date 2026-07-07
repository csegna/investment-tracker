import yfinance as yf


def get_current_price(ticker):
    """Look up the latest price for a ticker using Yahoo Finance.

    Returns the price as a float, or None if it couldn't be fetched
    (bad ticker, no internet connection, etc).
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if data.empty:
            return None
        return float(data["Close"].iloc[-1])
    except Exception:
        return None
