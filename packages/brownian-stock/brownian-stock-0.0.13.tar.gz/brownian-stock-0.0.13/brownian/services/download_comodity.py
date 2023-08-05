

import io
import os

import pandas as pd
import requests

from ..models.index_series import IndexSeries
from ..repository import IndexCsvRepository, RepositoryPath


def download_mizuho() -> list:
    """ ミズホのホームページから為替情報をダウンロードする
    """
    targets = [
        "USD",
        "EUR",
        "CNY"
    ]

    url = "https://www.mizuhobank.co.jp/market/csv/quote.csv"
    resp = requests.get(url)
    text = resp.text

    stream = io.StringIO(text)

    df = pd.read_csv(stream, skiprows=2)
    df.columns.values[0] = "Date"

    dates = pd.to_datetime(df["Date"]).dt.date
    results = {}
    for col in targets:
        price = pd.to_numeric(df[col], errors="coerce")
        series = IndexSeries(dates, price)
        results[col] = series
    return results


if __name__ == "__main__":
    index_dict = download_mizuho()

    path = RepositoryPath(os.path.expanduser("~/Document/jquants2"))
    repository = IndexCsvRepository(path)
    for key, series in index_dict.items():
        repository.save(key, series)

