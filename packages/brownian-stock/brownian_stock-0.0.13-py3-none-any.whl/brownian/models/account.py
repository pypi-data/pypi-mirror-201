
import datetime
import logging
from typing import Optional

from .. import const
from ..services import trading
from .abstract_model import AbstractModel
from .return_map import ReturnMap
from .stock_set import StockSet

logger = logging.getLogger(__name__)


class OpenToOpenLongShortAccount(AbstractModel):

    """ 当日寄りで買い, 翌日寄りでポジションを解放する
    """

    def __init__(self, stock_set: StockSet, log_dir: Optional[str] = None, top_n: int = 10) -> None:
        super().__init__(stock_set, log_dir)
        self.top_n = top_n

    def name(self) -> str:
        return "OpenToOpenLongShort"

    def trade(self, trade_date: datetime.date) -> None:
        raise NotImplementedError("This method can't call")

    def execute(self, trade_date: datetime.date, return_map: ReturnMap) -> None:
        """
        """
        capacity = self.margin(trade_date)
        logger.info(f"{self.name()}: capacity is {capacity}")

        if capacity < 0:
            logger.info(f"{self.name()}: you are bankrupt!!")
            return

        # 寄せで所有している株をすべて精算
        self.log("Reset the position.")
        self.sell_all_if_possible(trade_date, const.COL_OPEN)
        self.buy_all_if_possible(trade_date, const.COL_OPEN)

        # 寄せで新たにポジションを形成
        capacity = self.margin(trade_date)
        self.log("Execute long short trading.")
        order = trading.long_short_trading(capacity, trade_date, self.stock_set, return_map, const.COL_OPEN, reverse_order=False, top_n=self.top_n)
        trading.execute_order(self, trade_date, order, timing=const.COL_OPEN)


class OpenToOpenLongAccount(AbstractModel):

    def __init__(self, stock_set: StockSet, log_dir: Optional[str] = None, top_n: int = 10) -> None:
        super().__init__(stock_set, log_dir)
        self.top_n = top_n

    def name(self) -> str:
        return "OpenToOpenLong"

    def trade(self, trade_date: datetime.date) -> None:
        raise NotImplementedError("This method can't call")

    def execute(self, trade_date: datetime.date, return_map: ReturnMap) -> None:
        """
        """
        capacity = self.margin(trade_date)
        logger.info(f"{self.name()}: capacity is {capacity}")

        if capacity < 0:
            logger.info(f"{self.name()}: you are bankrupt!!")
            return
        # 寄せで所有している株をすべて精算
        self.log("Reset the position.")
        self.sell_all_if_possible(trade_date, const.COL_OPEN)

        # 寄せで新たにポジションを形成
        capacity = self.margin(trade_date)
        self.log("Execute long short trading.")
        order = trading.long_only_trading(capacity, trade_date, self.stock_set, return_map, const.COL_OPEN, reverse_order=False, top_n=self.top_n)
        trading.execute_order(self, trade_date, order, timing=const.COL_OPEN)


class OpenToOpenShortAccount(AbstractModel):

    def __init__(self, stock_set: StockSet, log_dir: Optional[str] = None, top_n: int = 10) -> None:
        super().__init__(stock_set, log_dir)
        self.top_n = top_n

    def name(self) -> str:
        return "OpenToOpenShort"

    def trade(self, trade_date: datetime.date) -> None:
        raise NotImplementedError("This method can't call")

    def execute(self, trade_date: datetime.date, return_map: ReturnMap) -> None:
        """
        """
        capacity = self.margin(trade_date)
        logger.info(f"{self.name()}: capacity is {capacity}")

        if capacity < 0:
            logger.info(f"{self.name()}: you are bankrupt!!")
            return
        # 寄せで所有している株をすべて精算
        self.log("Reset the position.")
        self.sell_all_if_possible(trade_date, const.COL_OPEN)

        # 寄せで新たにポジションを形成
        capacity = self.margin(trade_date)
        self.log("Execute short trading.")
        order = trading.short_only_trading(capacity, trade_date, self.stock_set, return_map, const.COL_OPEN, reverse_order=False, top_n=self.top_n)
        trading.execute_order(self, trade_date, order, timing=const.COL_OPEN)


class OpenToCloseLongShortAccount(AbstractModel):

    def __init__(self, stock_set: StockSet, log_dir: Optional[str] = None, top_n: int = 10) -> None:
        super().__init__(stock_set, log_dir)
        self.top_n = top_n

    def name(self) -> str:
        return "OpenToCloseLongShort"

    def trade(self, trade_date: datetime.date) -> None:
        raise NotImplementedError("This method can't call")

    def execute(self, trade_date: datetime.date, return_map: ReturnMap) -> None:
        """
        """
        capacity = self.margin(trade_date)
        logger.info(f"{self.name()}: capacity is {capacity}")

        if capacity < 0:
            logger.info(f"{self.name()}: you are bankrupt!!")
            return

        # 寄せでポジションを形成
        order = trading.long_short_trading(capacity, trade_date, self.stock_set, return_map, const.COL_OPEN, reverse_order=False, top_n=self.top_n)
        trading.execute_order(self, trade_date, order, timing=const.COL_OPEN)

        # 引きで全てのポジションを解放
        self.buy_all_if_possible(trade_date, const.COL_CLOSE)
        self.sell_all_if_possible(trade_date, const.COL_CLOSE)


