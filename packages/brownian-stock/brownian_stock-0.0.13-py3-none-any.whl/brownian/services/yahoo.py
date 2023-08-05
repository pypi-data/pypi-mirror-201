
import datetime

import yfinance as yf

from ..models.index_series import IndexSeries

CURRENCY_USD_JPY = "JPY=X"
CURRENCY_EUR_JPY = "EURJPY=X"
CURRENCY_AUD_JPY = "AUDJPY=X"

INDEX_DJI = "^DJI"
INDEX_SP500 = "^GSPC"
INDEX_NIKKEI = "^N225"

INDEX_DJ_COMODITY = "^DJCI"
INDEX_MSCI_EMERGING = "MME=F"

BOND_AMERICA_5Y = "^FVX"
BOND_AMERICA_10Y = "^TNX"

COMODITY_CRUDE_OIL = "CL=F"
COMODITY_GOLD = "GC=F"


def download_index(bond_type: str, start: datetime.date, end: datetime.date) -> IndexSeries:
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    df = yf.download(tickers=bond_type, start=start_str, end=end_str)
    df.reset_index(inplace=True)

    dates = df["Date"].dt.date.to_list()
    close = df["Close"].to_list()

    index = IndexSeries(dates, close)
    return index


if __name__ == "__main__":
    start = datetime.date(2017, 1, 1)
    end = datetime.date(2023, 3, 22)
    index = download_index(COMODITY_GOLD, start, end)
    index.show_figure()
