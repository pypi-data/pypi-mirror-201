
import copy
import datetime
import math
from typing import Any, List, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import polars as pl

from .. import const
from .abstract_series import AbstractSeries


class IndexSeries(AbstractSeries):

    """ 指数の時系列情報を管理するクラス
    """

    def __init__(self, date_ls :Sequence[datetime.date], value_ls: Sequence[Any]) -> None:
        # 入力のチェック
        if len(date_ls) != len(value_ls):
            raise ValueError("`date_ls` and `value_ls` must be same size.")
        for d in date_ls:
            if type(d) != datetime.date:
                raise ValueError(f"`date_ls` must be the sequense of datetime.date. Given value `{d}` is of type {type(d)}.")

        df = pl.DataFrame({
            const.COL_DATE: date_ls,
            const.COL_INDEX_VALUE: value_ls
        })
        df = df.sort(const.COL_DATE)
        super().__init__(df)

    def get_value(self, target_date: datetime.date) -> Any:
        return super().get_value(target_date, const.COL_INDEX_VALUE)

    def to_list(self) -> List[Any]:
        return self._df[const.COL_INDEX_VALUE].to_list()

    def to_array(self) -> np.ndarray[Any]:
        return self._df[const.COL_INDEX_VALUE].to_numpy()

    def to_series(self, to_polars:bool = False) -> Union[pl.Series, pd.Series]:
        if to_polars:
            return self._df[const.COL_INDEX_VALUE]
        return self._df[const.COL_INDEX_VALUE].to_pandas()

    def pct_change(self):
        """ 自身の前日比を取った新しいIndexSeriesを作成する

        Returns:
            IndexSeries: 前日比を取った新しいIndex
        """
        new_index = copy.copy(self)
        new_index._df = new_index._df.with_columns(
            pl.col(const.COL_INDEX_VALUE).pct_change().fill_null(0)
        )
        return new_index

    def show_figure(self) -> None:
        fig = plt.figure()
        ax = fig.add_subplot()
        x = self._df[const.COL_DATE].to_list()
        y = self._df[const.COL_INDEX_VALUE].to_list()
        ax.plot(x, y)
        plt.show()
