

"""
universe.py
====================
特定の分類の銘柄を抽出するためのクラス群.
各Universeに収録される銘柄は2023/1/3時点で広報されているデータ
各分類の詳細は以下のURLを参照.

https://www.jpx.co.jp/markets/indices/line-up/files/fac_12_size.pdf


Usage:
>> # TopixCore30のみを抽出する場合
>> universe_filter = TopixCore30()
>> stock_set = stock_set.filter(universe_filter)
"""

import pathlib

import pandas as pd

from ..models.stock_series import StockSeries

TOPIX_CORE_30 = "TOPIX Core30"
TOPIX_LARGE_70 = "TOPIX Large70"
TOPIX_MID_400 = "TOPIX Mid400"
TOPIX_SMALL_1 = "TOPIX Small 1"
TOPIX_SMALL_2 = "TOPIX Small 2"


class TopixBase:
    
    """ 抽象クラス
    """

    def __init__(self):
        csv_path = pathlib.Path(__file__).parent.parent / "data" / "topix_universe.csv"
        self.topix_df = pd.read_csv(csv_path)
        self.topix_df["Code"] = self.topix_df["Code"].astype(str)

    def get_code_list(self, code_type):
        filter_df = self.topix_df[self.topix_df["IndexSector"] == code_type]
        return filter_df["Code"].tolist()


class TopixCore30(TopixBase):

    """ TopixCore30の銘柄のみを抽出する
    """

    def __init__(self):
        super().__init__()
        self.code_list = self.get_code_list(TOPIX_CORE_30)

    def __call__(self, stock_serie):
        return stock_serie.stock_code in self.code_list

    def name(self):
        return TOPIX_CORE_30


class TopixLarge70(TopixBase):

    """ TopixLarge70の銘柄のみを抽出する
    """

    def __init__(self):
        super().__init__()
        self.code_list = self.get_code_list(TOPIX_LARGE_70)

    def __call__(self, stock_serie):
        return stock_serie.stock_code in self.code_list

    def name(self):
        return TOPIX_LARGE_70




class TopixMid400(TopixBase):

    """ TopixMid400の銘柄のみを抽出する
    """

    def __init__(self):
        super().__init__()
        self.code_list = self.get_code_list(TOPIX_MID_400)

    def __call__(self, stock_serie):
        return stock_serie.stock_code in self.code_list

    def name(self):
        return TOPIX_MID_400


class TopixSmall1(TopixBase):

    """ TopixSmall1の銘柄のみを抽出する
    """

    def __init__(self):
        super().__init__()
        self.code_list = self.get_code_list(TOPIX_SMALL_1)

    def __call__(self, stock_serie):
        return stock_serie.stock_code in self.code_list

    def name(self):
        return TOPIX_SMALL_1


class TopixSmall2(TopixBase):

    """ TopixSmall2の銘柄のみを抽出する
    """

    def __init__(self):
        super().__init__()
        self.code_list = self.get_code_list(TOPIX_SMALL_2)

    def __call__(self, stock_serie):
        return stock_serie.stock_code in self.code_list

    def name(self):
        return TOPIX_SMALL_2


class Topix100:

    """ Topix100を表すUniverse
    Topix100 = TopixCore30 + TopixLarge70
    """

    def __init__(self):
        self.core30 = TopixCore30()
        self.large70 = TopixLarge70()

    def __call__(self, stock_series):
        if self.core30(stock_series):
            return True
        if self.large70(stock_series):
            return True
        return False
    
    def name(self):
        return "Topix100"


class Topix500:

    """ Topix500を表すUniverse
    Topix500 = TopixCore30 + TopixLarge70 + TopixMid400
    """

    def __init__(self):
        self.core30 = TopixCore30()
        self.large70 = TopixLarge70()
        self.mid400  =TopixMid400()

    def __call__(self, stock_series):
        if self.core30(stock_series):
            return True
        if self.large70(stock_series):
            return True
        if self.mid400(stock_series):
            return True
        return False

    def name(self):
        return "Topix500"


class Topix1000:

    """ Topix1000を表すUniverse
    Topix1000 = TopixCore30 + TopixLarge70 + TopixMid400 + TopixSmall1
    """

    def __init__(self):
        self.core30 = TopixCore30()
        self.large70 = TopixLarge70()
        self.mid400  =TopixMid400()
        self.small1 = TopixSmall1()

    def __call__(self, stock_series):
        if self.core30(stock_series):
            return True
        if self.large70(stock_series):
            return True
        if self.mid400(stock_series):
            return True
        if self.small1(stock_series):
            return True
        return False

    def name(self):
        return "Topix1000"

