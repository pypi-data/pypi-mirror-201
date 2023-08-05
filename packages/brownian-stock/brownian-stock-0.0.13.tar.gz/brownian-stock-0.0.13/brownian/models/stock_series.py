
import datetime
import logging
import pathlib
from typing import Any, List, Optional, Union

import numpy as np
import pandas as pd
import polars as pl

from .. import const
from .abstract_series import AbstractSeries
from .pct_change_series import PctChangeSeries
from .sector_code import build_sector_code

logger = logging.getLogger(__name__)


class StockSeries(AbstractSeries):
    """
    Note:
        ドリフトやボラティリティの推定についての詳細は以下のURLを参照
        http://www.na.scitec.kobe-u.ac.jp/~yamamoto/lectures/computationalfinance/BS_verification.PDF
    """

    AVAILABLE_KEYS = [
        const.COL_DATE,
        const.COL_CLOSE,
        const.COL_OPEN,
        const.COL_LOW,
        const.COL_HIGH,
        const.COL_TRADING_VOLUME,
        const.COL_TURNOVER_VALUE,
    ]

    """ StockSeries - ある銘柄の時系列価格情報

    Args:
        df(pl.DataFrame): JQuantsから配信されたCSVデータ
    """

    def __init__(self, df: pl.DataFrame):
        # データの読み込み
        df = df.with_columns(
            pl.col(const.COL_DATE).str.strptime(pl.Date, fmt="%Y-%m-%d")
        )
        df = df.sort(const.COL_DATE)
        df = clean_dataframe(df)
        super().__init__(df)

        if len(self._df) == 0:
            raise ValueError("DataFrame contains No valid data.")

        # 特徴量
        self.stock_code = str(self._df[-1, const.COL_STOCK_CODE]).zfill(5)
        self.company_name = str(self._df[-1, const.COL_COMPANY_NAME])
        self.market_type = str(self._df[-1, const.COL_MARKET])

        self.sector = build_sector_code(int(self._df[-1, const.COL_SECTOR]))
        self.sector_detail = str(self._df[-1, const.COL_SECTOR_DETAIL])

    def __repr__(self) -> str:
        return f"StockSeries {self.stock_code} - {self.company_name}"

    def size(self) -> int:
        return len(self._df)

    def show(self) -> None:
        print(self._df.head())

    def day_summary(self, target_date :datetime.date) -> str:
        """ 指定した日の株価の概略を示す文字列を取得する
        Args:
            target_date(datetime.date): 対象日
        """
        df = self._df.filter(pl.col(const.COL_DATE) == target_date)
        opening = df[0, const.COL_OPEN]
        closing = df[0, const.COL_CLOSE]
        high = df[0, const.COL_HIGH]
        low = df[0, const.COL_LOW]

        text = f"O: {opening:.1f}, C: {closing:.1f}, H: {high:.1f}, L: {low:.1f}"
        return text

    def pct_change(self) -> PctChangeSeries:
        return PctChangeSeries(self)

    def to_list(self, key: str) -> List[Any]:
        if key not in self.AVAILABLE_KEYS:
            raise ValueError(f"Unknown key {key}")
        return self._df[key].to_list()

    def to_array(self, key: str) -> np.ndarray[Any, Any]:
        if key not in self.AVAILABLE_KEYS:
            raise ValueError(f"Unknown key {key}")
        return self._df[key].to_numpy()

    def to_series(self, key: str, as_polars :bool = False) -> Union[pl.Series, pd.Series]:
        if key not in self.AVAILABLE_KEYS:
            raise ValueError(f"Unknown key {key}")
        if as_polars:
            return self._df[key]
        return self._df[key].to_pandas()

    def to_array_view(self, key:str) -> np.ndarray[Any, Any]:
        """ Return numpy like view. This method DON'T copy array.
        So be careful when use.
        """
        if key not in self.AVAILABLE_KEYS:
            raise ValueError(f"Unknown key {key}")
        return self._df[key].view()

    def opening_price(self, target_date: datetime.date) -> Optional[float]:
        """ 指定した日の始値を返す
        """
        v = self.get_value(target_date, const.COL_OPEN)
        try:
            return float(v)
        except Exception as e:
            logger.exception(e)
            return None

    def closing_price(self, target_date: datetime.date) -> Optional[float]:
        """ 指定した日の終値を返す
        """
        v = self.get_value(target_date, const.COL_CLOSE)
        try:
            return float(v)
        except Exception as e:
            logger.exception(e)
            return None

    def has_record(self, target_date: datetime.date) -> bool:
        """ target_dateの情報を持っているかどうか

        Args:
            target_date(datetime.date): 確認したい対象の日付
        Return:
            bool: 指定した日付のデータを持っていたらTrue
        """
        idx = self._binary_search_left(target_date)
        if idx == len(self._df):
            return False
        if self._df[idx, const.COL_DATE] == target_date:
            return True
        return False


def clean_dataframe(df: pl.DataFrame) -> pl.DataFrame:
    """ 読み込んだDataFrmeの型を整形する.
    """
    # ゼロで補完する列
    zero_fill_columns = [
        const.COL_TRADING_VOLUME,
        const.COL_TURNOVER_VALUE
    ]

    # 前日価格で補完する列
    forward_fill_columns = [
        const.COL_OPEN,
        const.COL_CLOSE,
    ]

    # 終値で補完する列
    close_fill_columns = [
        const.COL_LOW,
        const.COL_HIGH
    ]

    # ルールにしたがって欠損を補完
    for col in zero_fill_columns:
        df = df.with_columns([
            pl.col(col).fill_null(0)
        ])

    for col in forward_fill_columns:
        df = df.with_columns([
            pl.col(col).fill_null(strategy="forward")
        ])

    for col in close_fill_columns:
        df = df.with_columns([
            pl.when(pl.col(col).is_null())
              .then(pl.col(const.COL_CLOSE))
              .otherwise(pl.col(col))
              .alias(col)
        ])

    # 頭の欠損などは削除できないので削除
    df = df.drop_nulls()
    return df


def load_stock_series(csv_path: Union[str, pathlib.Path]) -> StockSeries:
    df = pl.read_csv(csv_path)
    return StockSeries(df)
