
import copy

import numpy as np
import polars as pl

from .. import const
from ..models.index_series import IndexSeries
from ..models.pct_change_series import PctChangeSeries
from ..models.stock_series import StockSeries


def neutralize_stock(stock_series: StockSeries | PctChangeSeries, index_series: IndexSeries,
                     columns: None | list=None, proportion:float=1.0):
    """ IndexSereisで中立化したStockSeriesを作成する
    Args:
        stock_series(StockSeries): 中立化の対象とする株価
        index_series(IndexSeries): 中立化の基準となる系列データ
    """
    stock_series = copy.copy(stock_series)
    index_array = index_series.to_array()

    if columns is None:
        columns = [
            const.COL_CLOSE,
            const.COL_OPEN,
            const.COL_HIGH,
            const.COL_LOW
        ]

    df = stock_series._df
    for col in columns:
        base_array = stock_series.to_array(col)
        neutralize_array = neutralize_series(base_array, index_array, proportion=proportion)
        df = df.with_columns(
            pl.Series(name=col, values=neutralize_array)
        )
    stock_series._df = df
    return stock_series


def neutralize_index(index_series: IndexSeries, by: IndexSeries,
                     columns: None | list=None, proportion:float=1.0):
    """ IndexSereisで中立化したIndexSeriesを作成する
    Args:
        stock_series(IndexSeries): 中立化の対象とする株価
        index_series(IndexSeries): 中立化の基準となる系列データ
    """
    index_series = copy.copy(index_series)
    df = index_series._df

    base_array = index_series.to_array()
    by_array = by.to_array()

    neutralize_array = neutralize_series(base_array, by_array, proportion=proportion)
    df = df.with_columns(
        pl.Series(name=const.COL_INDEX_VALUE, values=neutralize_array)
    )
    index_series._df = df
    return index_series


def neutralize_series(series: np.ndarray, by: np.ndarray, proportion: float = 1.0):
   # https://yaakublog.com/numerai-feature-neutralization
   #scores = series.values.reshape(-1, 1)
   #exposures = by.values.reshape(-1, 1)
   # this line makes series neutral to a constant column so that it's centered and for sure gets corr 0 with exposures
   by = np.hstack(
       (by.reshape(-1, 1), np.array([np.mean(series)] * len(by)).reshape(-1, 1)))
 
   correction = proportion * (by.dot(
       np.linalg.lstsq(by, series, rcond=None)[0]))

   corrected_scores = series - correction
   neutralized = corrected_scores.ravel()
   return neutralized
