""" 実際の売買のシミュレーションを提供する
"""

import abc
import datetime
import logging
import math
import pathlib
from collections import defaultdict
from typing import DefaultDict, Optional

from .. import const
from .order import Order
from .return_map import ReturnMap
from .stock_set import StockSet


class MarginExceededError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return self.message


class AbstractModel(abc.ABC):

    """ 取引モデルを表現するクラス

    ## モデル構築によく使う関数
    buy: 特定の銘柄を購入する.
    sell: 特定の銘柄を売却する.

    """

    def __init__(self, stock_set: StockSet, log_dir: Optional[str] = None) -> None:
        self.stock_set = stock_set
        self.current_position :DefaultDict[str, int] = defaultdict(int)  # code => volume

        # self.cash :Optional[int] = None  # 所有している現金(売ると増える, 買うと減る数字)
        self.cash = 0

        # ログ周りの設定
        now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
        log_filename = f"trade_{now_str}.log"
        if not log_dir:
            self.log_path = pathlib.Path("./") / log_filename
        else:
            self.log_path = pathlib.Path(log_dir) / log_filename

        # ロガーを初期化
        self.logger = logging.getLogger(self.name())

    @abc.abstractmethod
    def name(self) -> str:
        """ モデルの名前
        """
        return "abstract"

    def init_state(self, margin: int) -> None:
        self.cash = margin

    @abc.abstractmethod
    def trade(self, trade_date: datetime.date) -> Optional[ReturnMap]:
        """ 対象日における取引戦略を実装する
        """
        pass

    @abc.abstractmethod
    def execute(self, trade_date: datetime.date, return_map: ReturnMap) -> None:
        """ orderを執行する
        """
        pass

    def day_close(self, target_date: datetime.date) -> None:
        """ 日が終わるときの処理
        """
        date_str = target_date.strftime("%Y-%m-%d")
        valuation = self.valuation(target_date)
        self.log(f"{date_str} closed. Current valuation: {valuation}")

    def buy(self, target_date: datetime.date, code: str, num: int, price :Optional[float] = None) -> None:
        """ 指定したコードの株をtarget_dateの始値で購入する.
        """
        if num < 0:
            raise ValueError("num must me a postive number.")
        target_stock = self.stock_set.get_stock(code)
        target_stock.day_summary(target_date)

        if price is None:
            price = target_stock.opening_price(target_date)

        brand_name = target_stock.company_name
        shrink_num = 0
        expand_num = num

        # ポジションの拡大料と縮小料を計算
        current_position = self.current_position[code]
        if current_position < 0:
            shrink_num = min(abs(current_position), abs(num))
            expand_num -= shrink_num

        total_amount = abs(expand_num * price)
        margin = self.margin(target_date)
        if total_amount > margin:
            self.log(f"Over magin when you call `buy`. Total Amount: {total_amount}, Margin: {margin}")
            raise MarginExceededError("Over margin.")

        # ポジションと取引額を記録する
        if abs(shrink_num) > 0:
            self.log(f"{target_date} Buy {brand_name} x {shrink_num} at {price} Yen (Positoin Shrink)")
        if abs(expand_num) > 0:
            self.log(f"{target_date} Buy {brand_name} x {expand_num} at {price} Yen (Positoin Expand)")

        # ポジションと取引額を記録する
        self.current_position[code] += num
        self.cash -= num * price

    def sell(self, target_date: datetime.date, code: str, num: int, price: Optional[int] = None) -> None:
        """ 指定したコードの株をtarget_dateの始値で購入する.
        """
        if num < 0:
            raise ValueError("num must me a postive number.")
        target_stock = self.stock_set.get_stock(code)

        if price is None:
            price = target_stock.opening_price(target_date)
        if math.isnan(price):
            raise RuntimeError(f"Can't sell {code}, because there is no trade on {target_date}")

        brand_name = target_stock.company_name
        shrink_num = 0
        expand_num = num
        current_position = self.current_position[code]

        # ポジションの拡大料と縮小料を計算
        current_position = self.current_position[code]
        if current_position > 0:
            shrink_num = min(abs(current_position), abs(num))
            expand_num -= shrink_num

        margin = self.margin(target_date)
        total_sell = expand_num * price
        if abs(total_sell) > self.margin(target_date):
            self.log("Over magin when you call `sell`")
            raise MarginExceededError(f"Over margin. Available margin is {margin} - You try to sell {total_sell}.")

        # ポジションと取引額を記録する
        if abs(shrink_num) > 0:
            self.log(f"{target_date} Sell {brand_name} x {shrink_num} at {price}Yen (Positoin Shrink)")
        if abs(expand_num) > 0:
            self.log(f"{target_date} Sell {brand_name} x {expand_num} at {price}Yen (Positoin Expand)")

        self.current_position[code] -= num
        self.cash += num * price

    def sell_all_if_possible(self, target_date: datetime.date, timing: str = const.COL_OPEN) -> None:
        """ ポジションを持っている株をすべて反対取引で売却する.
        対象の日に値がついていない場合には売却できないので保持し続ける
        """
        if timing not in [const.COL_OPEN, const.COL_CLOSE]:
            raise ValueError("You can specify either COL_OPEN or COL_CLOSE as `timing`")

        self.log(f"Sell all called on {timing}")
        for code, num in self.current_position.items():
            try:
                stock = self.stock_set.get_stock(code)
                price = stock.latest_value(timing, at=target_date)
                if num > 0:
                    self.sell(target_date, code, abs(num), price)
            except Exception as e:
                self.logger.exception(e)
                continue

    def buy_all_if_possible(self, target_date: datetime.date, timing :str = const.COL_OPEN) -> None:
        """ ポジションを持っている株をすべて反対取引で購入する.
        対象の日に値がついていない場合には売却できないので保持し続ける
        """

        if timing not in [const.COL_OPEN, const.COL_CLOSE]:
            raise ValueError("You can specify either COL_OPEN or COL_CLOSE as `timing`")

        self.log(f"Buy all called on {timing}")
        for code, num in self.current_position.items():
            try:
                stock = self.stock_set.get_stock(code)
                price = stock.latest_value(timing, at=target_date)
                if num < 0:
                    self.buy(target_date, code, abs(num), price)
            except Exception as e:
                self.logger.exception(e)
                continue

    def available_buy_volume(self, trade_date: datetime.date, code: str) -> int:
        target_stock = self.stock_set.get_stock(code)
        price = target_stock.opening_price(trade_date)
        if price is None:
            return 0
        num = self.buying_power // price
        num = num // 100 * 100
        if math.isnan(num):
            raise ValueError(f"Failed to compute buy volume. Price: {price}, Num: {num}")
        return num

    def valuation(self, trade_date: datetime.date, by_opening: bool = False) -> int:
        """ 評価額
        指定した日の終値で評価額を計算する
        """
        stock_valuation = 0
        for code, num in self.current_position.items():
            if num == 0:
                continue
            target_stock = self.stock_set.get_stock(code)
            closing_price = target_stock.latest_value(const.COL_CLOSE, at=trade_date)
            stock_valuation += closing_price * num
        return self.cash + stock_valuation

    def margin(self, trade_date: datetime.date) -> int:
        """ 保証金残量
        指定した日の始値で証拠金残量を計算する
        合計の資産から所有している株価の絶対額を引いたもの
        """
        valuation = self.cash
        stock_abs = 0

        for code, num in self.current_position.items():
            if num == 0:
                continue
            target_stock = self.stock_set.get_stock(code)
            opening_price = target_stock.latest_value(const.COL_OPEN, at=trade_date)

            # 市場が休みの日は最後の日の価格を利用する
            valuation += opening_price * num
            stock_abs += abs(opening_price * num)
        return max(valuation - stock_abs, 0)

    def log(self, msg: str) -> None:
        self.logger.info(msg)


class TopixBaselineModel(AbstractModel):

    def __init__(self, stock_set: StockSet, log_dir: Optional[str] = None) -> None:
        super().__init__(stock_set, log_dir)
        self.initialized = False

    def name(self) -> str:
        return "TopixBaselineModel"

    def trade(self, trade_date: datetime.date) -> Optional[ReturnMap]:
        order = Order()
        if not self.initialized and self.stock_set.get_stock("13080").has_record(trade_date):
            num = self.available_buy_volume(trade_date, "13080")
            order.buy("13080", num)
            self.initialized = True
        return order

    def execute(self, trade_date: datetime.date, return_map: ReturnMap) -> None:
        return super().execute(trade_date, return_map)

