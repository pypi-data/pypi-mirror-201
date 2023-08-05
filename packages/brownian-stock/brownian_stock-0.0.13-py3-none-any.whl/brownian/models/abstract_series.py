from __future__ import annotations

import copy
import datetime
import math
from typing import Any, Optional, Union

import pandas as pd
import polars as pl

from .. import const


class AbstractSeries:

    def __init__(self, df: pl.DataFrame):
        self._df = df

        # _binary_search_leftで使うインデックス
        # 生成にコストがかかるため、呼び出されたときに初めて初期化する
        # コピーする際にはかならず削除する必要がある
        self.__date_view = None

    def subset_by_range(self, start_date: datetime.date, end_date: datetime.date) -> AbstractSeries:
        """ Create subset of self in the specified range.
        """
        # 入力の型チェック
        if not isinstance(start_date, datetime.date):
            raise ValueError("start_date must be datetime.date.")
        if not isinstance(end_date, datetime.date):
            raise ValueError("end_date must be integer.")

        # 浅いコピー
        # DataFrameはコピーではなくて参照のみを保持する
        new_stock = self.copy()
        new_stock._df = self._df.filter(pl.col(const.COL_DATE).is_between(start_date, end_date))
        return new_stock

    def subset_by_recent_n_days(self, base_date: datetime.date, n_days:int) -> AbstractSeries:
        """ Create subset of self recent n-days from base_date.
        Subset doesn't include base_date.
        """

        # 入力の型チェック
        if not isinstance(base_date, datetime.date):
            raise ValueError("base_date must be datetime.date.")
        if not isinstance(n_days, int):
            raise ValueError("n_days must be integer.")

        try:
            idx = self._binary_search_left(base_date)
            if idx != len(self._df):
                df = self._df[:idx, :]
            if len(df) < n_days:
                raise ValueError("There was no data that satisfies the specified number of days.")
            # n_days分のデータを取得
            df = df[-n_days:]

            # 自分自身をコピー
            new_stock = self.copy()
            new_stock._df = df
            return new_stock
        except Exception:
            raise ValueError("There was no data that satisfies the specified number of days.")

    def subset_by_after_n_days(self, base_date: datetime.date, n_days: int) -> AbstractSeries:

        # 入力の型チェック
        if not isinstance(base_date, datetime.date):
            raise ValueError("base_date must be datetime.date.")
        if not isinstance(n_days, int):
            raise ValueError("n_days must be integer.")

        try:
            # n_days分のデータを取得
            idx = self._binary_search_left(base_date)
            if idx == len(self._df):
                raise ValueError("There was no data that satisfies the specified number of days.")

            df = self._df[idx:, :]
            if len(df) < n_days:
                raise ValueError("There was no data that satisfies the specified number of days.")
            df = df[:n_days]

            # 自分自身をコピー
            new_stock = self.copy()
            new_stock._df = df
            return new_stock
        except Exception:
            raise ValueError("There was no data that satisfies the specified number of days.")

    def copy(self) -> AbstractSeries:
        v = copy.copy(self)
        v.__date_view = None
        return v

    def dataframe(self, as_polars :bool = False) -> Union[pl.DataFrame, pd.DataFrame]:
        if as_polars:
            return self._df
        return self._df.to_pandas()

    def get_value(self, target_date: datetime.date, col: str) -> Any:
        try:
            idx = self._binary_search_left(target_date)
            if self._df[idx, const.COL_DATE] != target_date:
                return None
            value = self._df[idx, col]
            if math.isnan(value):
                value = None
            return value
        except Exception:
            return None

    def latest_value(self, col_name: str, at: Optional[datetime.date] = None) -> Any:
        """ Get latest value. If `at` is given, return latest value where d <= `at`.
        """
        if at is not None:
            next_date = at + datetime.timedelta(days=1)
            idx = self._binary_search_left(next_date) - 1
            if idx < 0:
                return None
            return self._df[idx, col_name]
        return self._df[-1, col_name]

    def oldest_value(self, col_name: str) -> Any:
        """ 一番古い情報を取得する
        """
        return self._df[0, col_name]

    def _binary_search_left(self, d: datetime.date) -> int:
        if self.__date_view is None:
            self.__date_view = self._df[const.COL_DATE].view()
        base_date_int = (d - datetime.date(1970, 1, 1)).days
        idx :int = self.__date_view.searchsorted(base_date_int, side="left")  # NOQA
        return int(idx)
