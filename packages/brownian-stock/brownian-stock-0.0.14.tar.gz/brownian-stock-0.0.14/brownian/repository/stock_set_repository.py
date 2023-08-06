
import polars as pl
import tqdm

from ..models.stock_series import StockSeries
from ..models.stock_set import StockSet
from .repository_path import RepositoryPath


class StockSetRepository:

    def __init__(self, repository_path: RepositoryPath):
        self.repository_path = repository_path

    def load(self, limit=None):
        stock_series_list = []
        dir_path = self.repository_path.stock_path
        filelist = list(dir_path.iterdir())

        if limit is not None:
            filelist = filelist[:limit]

        failed_ls = []
        for file in tqdm.tqdm(filelist):
            try:
                if not file.name.endswith(".csv"):
                    continue
                stock_series = load_stock_series(file)
                stock_series_list.append(stock_series)
            except Exception:
                failed_ls.append(file)
        for failed_file in failed_ls:
            self.log(f"[*] Failed to load {failed_file}")
        obj = StockSet(stock_series_list)
        return obj

    def log(self, msg):
        print(msg)


def load_stock_series(csv_path):
    df = pl.read_csv(csv_path)
    return StockSeries(df)
