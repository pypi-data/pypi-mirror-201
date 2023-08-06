
import datetime
import heapq
import logging
from typing import List, Optional, Tuple

from .. import const
from ..models.abstract_model import AbstractModel, MarginExceededError
from ..models.calendar import Calendar
from ..models.order import Order
from ..models.return_map import ReturnMap
from ..models.stock_series import StockSeries
from ..models.stock_set import StockSet

logger = logging.getLogger(__name__)


def execute_order(
        model: AbstractModel,
        trade_date: datetime.date,
        order: Order,
        timing: str = const.COL_CLOSE,
        shink_and_continue: bool = True) -> None:
    """ Orderに基づいて取引を執行する
    Args:
        trade_date(datetime.date): 取引対象日
        shink_and_continue(bool): Trueの場合, 取引可能料を超えた場合には取引量を削減して継続する
    """

    if timing not in [const.COL_CLOSE, const.COL_OPEN]:
        raise ValueError("`timing` must be either COL_CLOSE or COL_OPEN")
    # 取引を執行
    for code, num in order.buy_iter():
        while num > 0 and shink_and_continue:
            try:
                stock = model.stock_set.get_stock(code)
                price = stock.latest_value(timing, at=trade_date)
                model.buy(trade_date, code, num, price)
                break
            except MarginExceededError:
                num -= 100
    for code, num in order.sell_iter():
        while num > 0 and shink_and_continue:
            try:
                stock = model.stock_set.get_stock(code)
                price = stock.latest_value(timing, at=trade_date)
                model.sell(trade_date, code, num)
                break
            except MarginExceededError:
                num -= 100


def long_short_trading(trading_capacity: int, trade_date: datetime.date, subset: StockSet, result_map: ReturnMap,
                       timing: str, top_n:int = 5, reverse_order:bool = False, safety_margin:float = 0.99) -> Order:
    """ ロングショート戦略を行う補助関数
    対象日に値がついていない銘柄は事前にフィルタリングして取引の対象から外す.
    """
    margined_capacity = float(trading_capacity) * safety_margin
    buy_limit = int(margined_capacity // 2)
    sell_limit = int(margined_capacity - buy_limit)

    buy_order = long_only_trading(buy_limit, trade_date, subset, result_map, timing, top_n, reverse_order, safety_margin)
    sell_order = short_only_trading(sell_limit, trade_date, subset, result_map, timing, top_n, reverse_order, safety_margin)

    order = Order()
    for code, num in buy_order.buy_iter():
        order.buy(code, num)
    for code, num in sell_order.sell_iter():
        order.sell(code, num)
    return order


def long_only_trading(trading_capacity: int, trade_date: datetime.date, subset: StockSet, result_map: ReturnMap,
                      timing: str, top_n:int = 5, reverse_order:bool = False, safety_margin:float = 0.99) -> Order:
    """ ロングのみの取引を行うOrderを生成する
    対象日に値がついていない銘柄は事前にフィルタリングして取引の対象から外す.
    """
    calendar = Calendar.get_instance()
    reference_date = calendar.last_business_day(trade_date)

    buy_limit = float(trading_capacity) * safety_margin
    logger.debug(f"Reference date for {trade_date} is {reference_date}")

    # 前営業日に取引可能なsubset
    subset = subset.subset_by_available_at(reference_date)
    available_code = [s.stock_code for s in subset]
    logger.debug(f"Available set size on {trade_date}: {len(available_code)}")

    # 取引できない銘柄は省く
    ordred = result_map.ordered_code_list(asc=reverse_order)
    buy_ordred = [c for c in ordred if c in available_code]

    # 上位N件のみを抽出　
    logger.debug(f"Trade top {top_n} on {trade_date}")
    size = min(len(buy_ordred), top_n)
    buy_ordred = buy_ordred[:size]

    buy_heap :List[Tuple[int, str]] = []
    for code in buy_ordred:
        heapq.heappush(buy_heap, (0, code))
    logger.debug(f"Heap size for `buy`: {len(buy_heap)}")

    order = Order()
    # 買い取引
    while len(buy_heap) > 0:
        amount, code = heapq.heappop(buy_heap)
        stock = subset.get_stock(code)
        price = get_price(reference_date, stock, timing)
        if price is None:
            raise RuntimeError(f"Cant't trade {code}")

        num_limit = buy_limit // price
        if num_limit < 100:
            continue
        num = 100
        buy_limit -= num * price
        order.buy(code, num)
        heapq.heappush(buy_heap, (amount + price * num, code))
        logger.debug(f"Long-Short Trading Buy: {code} - {num}")
    return order


def short_only_trading(trading_capacity: int, trade_date: datetime.date, subset: StockSet, result_map: ReturnMap,
                       timing: str, top_n:int = 5, reverse_order:bool = False, safety_margin:float = 0.99) -> Order:
    """ ショートのみの取引戦略
    対象日に値がついていない銘柄は事前にフィルタリングして取引の対象から外す.
    """
    calendar = Calendar.get_instance()
    reference_date = calendar.last_business_day(trade_date)

    sell_limit = float(trading_capacity) * safety_margin
    logger.debug(f"Reference date for {trade_date} is {reference_date}")

    # 前営業日に取引可能なsubset
    subset = subset.subset_by_available_at(reference_date)
    available_code = [s.stock_code for s in subset]
    logger.debug(f"Available set size on {trade_date}: {len(available_code)}")

    # 取引できない銘柄は省く
    ordred = result_map.ordered_code_list(asc=reverse_order)
    sell_ordered = list(reversed([c for c in ordred if c in available_code]))

    # 上位N件のみを抽出　
    logger.debug(f"Trade top {top_n} on {trade_date}")
    size = min(len(sell_ordered), top_n)
    sell_ordered = sell_ordered[:size]

    sell_heap :List[Tuple[int, str]] = []
    for code in sell_ordered:
        heapq.heappush(sell_heap, (0, code))
    logger.debug(f"Heap size for `sell`: {len(sell_heap)}")

    order = Order()
    # 買い取引
    while len(sell_heap) > 0:
        amount, code = heapq.heappop(sell_heap)
        stock = subset.get_stock(code)
        price = get_price(reference_date, stock, timing)
        if price is None:
            raise RuntimeError(f"Cant't trade {code}")

        num_limit = sell_limit // price
        if num_limit < 100:
            continue
        num = 100
        sell_limit -= num * price
        order.sell(code, num)
        heapq.heappush(sell_heap, (amount + price * num, code))
        logger.debug(f"Long-Short Trading Buy: {code} - {num}")
    return order


def get_price(target_date: datetime.date, stock: StockSeries, timing :str) -> Optional[float]:
    if timing == const.COL_OPEN:
        return stock.opening_price(target_date)
    elif timing == const.COL_CLOSE:
        return stock.closing_price(target_date)
    else:
        raise ValueError("")
