

import os

import polars as pl

from .. import const
from ..models.index_series import IndexSeries
from .repository_path import RepositoryPath


class IndexCsvRepository:

    """ IndexSeriesの保存周りを管理するクラス
    """

    def __init__(self, repository_path: RepositoryPath) -> None:
        self.repository_path = repository_path

    def load(self, code: str) -> IndexSeries:
        """ 指定したコードのIndex
        """
        comodity_path = self.repository_path.comodity_path
        if not comodity_path.exists():
            raise IOError("Comodity directory doesn't exists.")
        filename = f"{code}.csv"
        filepath = comodity_path / filename

        df = pl.read_csv(filepath)
        df = df.with_columns(pl.col(const.COL_DATE).str.strptime(pl.Date, fmt="%Y-%m-%d"))

        dates = df[const.COL_DATE].to_list()
        values = df[const.COL_INDEX_VALUE].to_list()
        index_series = IndexSeries(dates, values)
        return index_series

    def save(self, code: str, index_series: IndexSeries) -> None:
        # コモディティ用のフォルダが存在しなかったら作成する　
        comodity_path = self.repository_path.comodity_path
        if not comodity_path.exists():
            os.makedirs(comodity_path)

        filename = f"{code}.csv"
        filepath = comodity_path / filename

        df = index_series.dataframe(as_polars=True)
        df.write_csv(filepath, datetime_format="%Y-%m-%d")
