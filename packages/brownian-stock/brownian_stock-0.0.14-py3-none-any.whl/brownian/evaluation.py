
import abc
import math

import numpy as np

from . import const

""" ある銘柄の評価値を管理するクラス群
"""


class StockEval:

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def __call__(self, target_stock):
        pass


class StockSetEval(abc.ABC):

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def __call__(self, stock_set):
        pass


class PercentageChangeStockEval(StockEval):

    """ 渡された期間の最初の日の始値と最後の日の終値から騰落率を計算する
    """

    def name(self):
        return "騰落率"

    def __call__(self, target_stock):
        start_price = target_stock.oldest_value(const.COL_OPEN) + 0.1
        end_price = target_stock.latest_value(const.COL_CLOSE)
        if np.isnan(start_price):
            return 0
        if np.isnan(end_price):
            return 0
        change_rate = end_price / start_price
        return change_rate

class PercentageChangeStockSetEval(StockSetEval):

    """ 与えられたStockSetの騰落率の平均を計算する
    """

    def name(self):
        return "騰落率"

    def __call__(self, stock_set):
        if len(stock_set) == 0:
            raise ValueError("stock_set must have at least one stock_series.")
        eval_obj =PercentageChangeStockEval()

        rate_sum = 0.
        rate_count = 0.
        for s in stock_set:
            rate = eval_obj(s)
            rate_sum += rate
            rate_count += 1
        return rate_sum / rate_count


class VolumeWeighedChangeStockSetEval(StockSetEval):
    """ 各銘柄の出来高で重み付けした騰落率
    """

    def name(self):
        return "重み付け平均騰落率"

    def __call__(self, stock_set):
        
        start_sum = 0
        close_sum = 0
        for s in stock_set:
            start_price = s.oldest_value(const.COL_OPEN)
            end_price = s.latest_value(const.COL_CLOSE)
            start_volume = s.oldest_value(const.COL_TRADING_VOLUME)
            end_volume = s.latest_value(const.COL_TRADING_VOLUME)
            start_sum += start_price * start_volume
            close_sum += end_price * end_volume
        return close_sum / start_sum


class VolatilityStockEval(StockEval):

    """ 渡された株価情報のボラティリティを計算します.
    """

    def __init__(self, target_col):
        self.target_col = target_col

    def __call__(self, stock):
        series = stock.df[self.target_col]
        series = series.apply(np.log)
        series = series - series.diff()
        series = series.dropna()
        std = np.std(series, ddof=1)
        return std

class VolatilityStockSetEval(StockEval):

    """ 渡された株価の集合に対してボラティリティの平均を計算します
    """

    def __init__(self, target_col):
        self.target_col = target_col

    def __call__(self, stock_set):
        eval_obj = VolatilityStockEval(self.target_col)
        std_sum = 0.
        divider = 0.
        for s in stock_set:
            std = eval_obj(s)
            std_sum += std
            divider += 1
        return std_sum / divider


class DriftStockEval(StockEval):

    def __init__(self, col_name=const.COL_OPEN):
        self.col_name = col_name

    def name(self):
        return "Drift"

    def __call__(self, target_stock):
        """ ブラック・ショールズモデルに基づきドリフトとボラティリティを推定する
        Return
            (float, float): ドリフトとボラティリティ
        """
        try:
            mu, std = blackshores_score(target_stock.df, self.col_name)
            return mu
        except RuntimeError as e:
            return -np.inf
        

class SigmaStockEval(StockEval):

    def __init__(self, col_name=const.COL_OPEN):
        self.col_name = col_name

    def name(self):
        return "Sigma"

    def __call__(self, target_stock):
        """ ブラック・ショールズモデルに基づきドリフトとボラティリティを推定する
        Return
            (float, float): ドリフトとボラティリティ
        """
        try:
            _, std = blackshores_score(target_stock.df, self.col_name)
            return std
        except RuntimeError as e:
            return np.inf



class DriftStockSetEval(StockSetEval):

    def __init__(self, col_name=const.COL_OPEN):
        self.col_name = col_name

    def name(self):
        return "Drift"

    def __call__(self, stock_set):
        eval_obj = DriftStockEval(self.col_name)
        rate_sum = 0.
        rate_count = 0.
        for s in stock_set:
            rate = eval_obj(s) * s.latest_value(const.COL_TRADING_VOLUME)
            if np.isnan(rate):
                continue
            rate_sum += rate
            rate_count += s.latest_value(const.COL_TRADING_VOLUME)
        return rate_sum / rate_count


class SigmaStockSetEval(StockSetEval):

    def __init__(self, col_name=const.COL_OPEN):
        self.col_name = col_name

    def name(self):
        return "Sigma"

    def __call__(self, stock_set):
        eval_obj = SigmaStockEval(self.col_name)
        rate_sum = 0.
        rate_count = 0.
        for s in stock_set:
            rate = eval_obj(s)
            if np.isnan(rate):
                continue
            rate_sum += rate
            rate_count += 1
        return rate_sum / rate_count


def blackshores_score(df, col_name):
    if len(df) < 2:
        raise RuntimeError("")

    try:
        # bar_rを計算
        r_list = []
        prev_price = None
        for _, row in df.iterrows():
            if prev_price is None:
                prev_price = float(row[col_name])
                continue
            # 時刻tにおける実現値を計算
            current_price = float(row[col_name])
            rt = math.log(current_price) - math.log(prev_price)

            # 値を更新
            r_list.append(rt)
            prev_price = current_price
        bar_r = sum(r_list) / len(r_list)

        # stdを計算
        std_list = []
        for rt in r_list:
            std_t = math.pow(rt - bar_r, 2)
            std_list.append(std_t)
        dof = len(r_list) - 1 # 自由度
        std = math.sqrt(sum(std_list)/dof)

        # muとsigmaを計算
        mu = bar_r + math.pow(std, 2) / 2
        return mu, std
    except Exception as e:
        raise RuntimeError("")