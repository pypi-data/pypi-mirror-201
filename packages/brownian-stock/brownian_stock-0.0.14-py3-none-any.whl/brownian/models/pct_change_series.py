
import numpy as np
import polars as pl

from .. import const
from .abstract_series import AbstractSeries


class PctChangeSeries(AbstractSeries):

    """ 銘柄の前日との差分を管理するクラス
    """

    AVAILABLE_KEYS = [
        const.COL_CLOSE,
        const.COL_OPEN,
        const.COL_LOW,
        const.COL_HIGH,
        const.COL_TRADING_VOLUME,
        const.COL_TURNOVER_VALUE,
    ]

    def __init__(self, stock):
        base_df = stock.dataframe(as_polars=True)
        base_df = base_df.select([
            pl.col(const.COL_DATE),
            pl.col(const.COL_OPEN).pct_change().fill_null(0),
            pl.col(const.COL_CLOSE).pct_change().fill_null(0),
            pl.col(const.COL_LOW).pct_change().fill_null(0),
            pl.col(const.COL_HIGH).pct_change().fill_null(0),
            pl.col(const.COL_TRADING_VOLUME).pct_change().fill_null(0),
            pl.col(const.COL_TURNOVER_VALUE).pct_change().fill_null(0)
        ])

        super().__init__(base_df)
        self.stock_code = stock.stock_code
        self.company_name = stock.company_name
        self.market_type = stock.market_type
        self.sector = stock.sector
        self.sector_detail = stock.sector_detail

    def to_list(self, key) -> list:
        return self._df[key].to_list()

    def to_array(self, key) -> np.ndarray:
        return self._df[key].to_numpy()

    def to_series(self, key) -> pl.Series:
        return self._df[key]
