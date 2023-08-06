
from __future__ import annotations

import datetime
import pathlib
from typing import List

import tqdm

from .stock_series import StockSeries, load_stock_series


def load_stock_set(dir_path, limit=None):
    """ CSVが格納されているパスを指定して初期化する
    """
    stock_series_list = []
    dir_path = pathlib.Path(dir_path)
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
        print(f"[*] Failed to load {failed_file}")
    obj = StockSet(stock_series_list)
    return obj


class StockSet:

    def __init__(self, stock_list: List[StockSeries]) -> None:
        self.set_stock_list(stock_list)

    def __iter__(self):
        return iter(self.stock_series_list)

    def __len__(self):
        return len(self.stock_series_list)

    def set_stock_list(self, new_stock_list: List[StockSeries]) -> None:
        self.stock_series_list = new_stock_list
        self.code_dict = {s.stock_code: s for s in new_stock_list}

    def stock_list(self):
        """ StockSeriesのリストを返す
        """
        return self.stock_series_list

    def get_stock(self, code) -> StockSeries:
        try:
            return self.code_dict[code]
        except KeyError:
            raise ValueError(f"Unexisting stock code. {code}")

    def filter(self, func) -> StockSet:
        """ 引数で与えられた関数に基づいてサブセットを作成する
        """
        filtered_ls = []
        for stock in self.stock_series_list:
            ok = func(stock)
            if not isinstance(ok, bool):
                raise ValueError("'func' must return boolean value.")
            if ok:
                filtered_ls.append(stock)
        new_subset = StockSet(filtered_ls)
        return new_subset

    def top_n(self, func, size: int, asc=False):
        """ 与えられたfuncでStockSeriesで評価を行い, 評価値の高いN銘柄のリストを返す
        デフォルトで降順で結果を返す.

        Args:
            func(function or StokcEval): StockSeriesの評価関数. 引数を一つだけ取る必要がある.
            size(int): 上位何件を抽出するかを表す整数.
        """
        scored_ls = []
        for s in self:
            score = func(s)
            scored_ls.append((score, s))
        scored_ls = sorted(scored_ls, key=lambda t: t[0], reverse=not asc)
        size = min(len(scored_ls), size)
        scored_ls = scored_ls[:size]
        result_ls = [s for _, s in scored_ls]
        return result_ls

    def pct_change(self) -> StockSet:
        """ 各銘柄の前日比を計算する.
        """
        ls = []
        for s in self:
            s = s.pct_change()
            ls.append(s)
        new_subset = StockSet(ls)
        return new_subset

    def subset_by_range(self, start_date: datetime.date, end_date: datetime.date) -> StockSet:
        """ 指定した日付の範囲でStockSeriesのsubsetを作成する

        Args:
            start_date(datetime.date): 抽出する期間の最初の日
            end_date(datetime.date): 抽出する期間の最後の日

        Returns:
            StockSet
        """
        if not isinstance(start_date, datetime.date):
            raise ValueError("'start_date' must be datetime.date")
        if not isinstance(end_date, datetime.date):
            raise ValueError("'end_date' must be datetime.date")
        stock_ls = []
        for stock in self.stock_series_list:
            clipped_stock = stock.subset_by_range(start_date, end_date)
            stock_ls.append(clipped_stock)
        new_subset = StockSet(stock_ls)
        return new_subset

    def subset_by_recent_n_days(self, base_date: datetime.date, n_days: int, ignore_error: bool = True) -> StockSet:
        """ 指定した日を含む直近のn日のsubsetを構成する.
        返す期間は[base_date - n_days, base_date)の半開区間なので, base_dateは含まない.
        """
        if not isinstance(base_date, datetime.date):
            raise ValueError("'base_date' must be datetime.date")
        if not isinstance(n_days, int):
            raise ValueError("'n_days' must be int")
        stock_ls = []
        for stock in self.stock_series_list:
            try:
                clipped_stock = stock.subset_by_recent_n_days(base_date, n_days)
                stock_ls.append(clipped_stock)
            except Exception as e:
                if not ignore_error:
                    raise e
        new_subset = StockSet(stock_ls)
        return new_subset

    def subset_by_after_n_days(self, base_date: datetime.date, n_days: int, ignore_error: bool = True) -> StockSet:
        """ 指定した日を含む直後のn日のsubsetを構成する.
        返す期間は[base_date, base_date+n_days)の半開区間なので, base_dateを含む
        """
        if not isinstance(base_date, datetime.date):
            raise ValueError("'base_date' must be datetime.date")
        if not isinstance(n_days, int):
            raise ValueError("'n_days' must be int")
        stock_ls = []
        for stock in self.stock_series_list:
            try:
                clipped_stock = stock.subset_by_after_n_days(base_date, n_days)
                if clipped_stock.check():
                    stock_ls.append(clipped_stock)
            except Exception as e:
                if not ignore_error:
                    raise e
        new_subset = StockSet(stock_ls)
        return new_subset

    def subset_by_available_at(self, target_date: datetime.date) -> StockSet:
        """ 指定した日に売買可能な銘柄のsubsetを構成する
        売買可能な銘柄とは以下２つの条件を満たす銘柄.
        1) 指定した日のレコードを持つこと
        2) 指定した日に始値と終値を持つこと
        """
        def available_stock(s: StockSeries) -> bool:
            if not s.has_record(target_date):
                return False
            if s.opening_price(target_date) is None:
                return False
            if s.closing_price(target_date) is None:
                return False
            return True
        return self.filter(available_stock)

    def neutralize(self, index_series, ignore_error=True):
        """ 所有する株価をすべてindex_seriesでneutralizeする

        Return:
            StockSet: 指定したindex_seriesでneutralizedしたStockSet
        """
        stock_ls = []
        for s in self.stock_series_list:
            try:
                new_s = s.neutralize(index_series)
                stock_ls.append(new_s)
            except Exception as e:
                if not ignore_error:
                    raise e
        new_subset = StockSet()
        new_subset.set_stock_list(stock_ls)
        return new_subset
