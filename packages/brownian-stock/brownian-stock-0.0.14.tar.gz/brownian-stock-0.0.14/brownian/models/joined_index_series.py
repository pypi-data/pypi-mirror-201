
from __future__ import annotations

import copy
import datetime
from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd
import polars as pl

from .. import const
from .abstract_series import AbstractSeries
from .index_series import IndexSeries


class JoinedIndexSeries(AbstractSeries):

    def __init__(self, index_dict: Dict[str, IndexSeries], how: str = "inner"):
        if len(index_dict) == 0:
            raise ValueError("Length of index_dict must be larger than 0")

        available_keys = []
        df_ls :List[pl.DataFrame] = []
        for key, index in index_dict.items():
            available_keys.append(key)
            df = index._df
            df = df.rename({const.COL_INDEX_VALUE: key})
            df_ls.append(df)

        base_df = df_ls.pop()
        while len(df_ls) > 0:
            poped_df = df_ls.pop()
            base_df = base_df.join(poped_df, on=const.COL_DATE, how=how)
        base_df = base_df.sort(const.COL_DATE)
        super().__init__(base_df)
        self.available_keys = available_keys

    def get_value(self, target_date: datetime.date, key: str) -> Any:
        if key not in self.available_keys:
            raise ValueError(f"Unknown key {key}")
        value: Any = super().get_value(target_date, key)
        return value

    def to_list(self, key: str) -> List[Any]:
        if key not in self.available_keys:
            raise ValueError(f"Unknown key {key}")
        value :List[Any] = self._df[key].to_list()
        return value

    def to_array(self, key: str) -> np.ndarray[Any, Any]:
        if key not in self.available_keys:
            raise ValueError(f"Unknown key {key}")
        value :np.ndarray[Any, Any] = self._df[key].to_numpy()
        return value

    def to_series(self, key: str, to_polars: bool = False) -> Union[pl.Series, pd.Series]:
        if key not in self.available_keys:
            raise ValueError(f"Unknown key {key}")
        if to_polars:
            return self._df[key]
        return self._df[key].to_pandas()

    def pct_change(self) -> JoinedIndexSeries:
        """ 自身の前日比を取った新しいIndexSeriesを作成する

        Returns:
            IndexSeries: 前日比を取った新しいIndex
        """
        new_index = copy.copy(self)

        # 欠損がある場合にはその前の値で補完する
        change_df = new_index._df.fill_null(strategy="forward")

        # 差分を計算して補完してしまった場所を元に戻す
        for col in self.available_keys:
            null_mask = new_index._df[col].is_null()
            change_df = change_df.with_columns(
                pl.col(col).pct_change()
            )
            change_df = change_df.with_columns(
                pl.when(null_mask).then(None).otherwise(pl.col(col)).alias(col)
            )
        change_df = change_df[1:]
        new_index._df = change_df
        return new_index
