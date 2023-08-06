
import datetime
import pathlib
import tempfile

import pytest

from brownian import (MarginExceededError, OpenToOpenLongShortAccount,
                      StockSet, load_stock_series)


def test_abstract_model() -> None:
    """ 信用取引をしない場合のテストケース
    """
    # 下準備
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = load_stock_series(filepath)
    stock_set = StockSet([stock_series])

    with tempfile.TemporaryDirectory() as dirname:
        model = OpenToOpenLongShortAccount(stock_set, dirname)
        model.init_state(1000000)

        # 株価の購入
        # 4/1の始値は2273.5
        # 3/31の終値は2286
        target_date = datetime.date(2022, 4, 1)
        model.buy(target_date, "86970", 100)

        assert model.margin(target_date) == 772650

        # 買付余力を超えた買い付け
        with pytest.raises(MarginExceededError):
            model.buy(target_date, "86970", 1000)

        # 株価の売却
        model.sell(target_date, "86970", 100)
        assert model.margin(target_date) == 1000000

        # 存在しない株価の売却
        with pytest.raises(ValueError):
            model.sell(target_date, "00000", 100)

        # マイナスの売買ができないことの確認
        with pytest.raises(ValueError):
            model.buy(target_date, "00000", -100)
        with pytest.raises(ValueError):
            model.sell(target_date, "00000", -100)

        # valuationが正しく計算できているか確認
        # valuationは終値で計算される
        model.buy(target_date, "86970", 100)
        assert model.valuation(target_date) == 1005000


def test_abstraction_model_sell() -> None:
    """ 信用売りから入る場合のテストケース
    """
    # 下準備
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = load_stock_series(filepath)
    stock_set = StockSet([stock_series])

    with tempfile.TemporaryDirectory() as dirname:
        model = OpenToOpenLongShortAccount(stock_set, dirname)
        model.init_state(1000000)

        # 株価の購入
        # 4/1の始値は2273.5
        # 4/1の終値は2323.5
        target_date = datetime.date(2022, 4, 1)
        model.sell(target_date, "86970", 100)
        assert model.margin(target_date) == 772650

        # valuationが正しいか検証
        assert model.valuation(target_date) == 995000

        # 証拠金を超えた売り
        # 買付余力を超えた買い付け
        with pytest.raises(MarginExceededError):
            model.sell(target_date, "86970", 1000)

        # 買い戻し
        model.buy(target_date, "86970", 100)
        assert model.margin(target_date) == 1000000
        assert model.valuation(target_date) == 1000000


def test_sell_all_as_possible() -> None:
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = load_stock_series(filepath)
    stock_set = StockSet([stock_series])

    with tempfile.TemporaryDirectory() as dirname:
        model = OpenToOpenLongShortAccount(stock_set, dirname)
        model.init_state(1000000)

        # 株価の購入
        # 4/1の始値は2273.5
        # 4/1の終値は2323.5
        target_date = datetime.date(2022, 4, 1)
        model.buy(target_date, "86970", 400)
        assert sum(model.current_position.values()) == 400

        # すべて精算
        model.sell_all_if_possible(target_date)
        assert model.margin(target_date) == 1000000
        assert sum(model.current_position.values()) == 0


def test_buy_all_as_possible() -> None:
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = load_stock_series(filepath)
    stock_set = StockSet([stock_series])

    with tempfile.TemporaryDirectory() as dirname:
        model = OpenToOpenLongShortAccount(stock_set, dirname)
        model.init_state(1000000)

        # 株価の購入
        # 4/1の始値は2273.5
        # 4/1の終値は2323.5
        target_date = datetime.date(2022, 4, 1)
        model.sell(target_date, "86970", 400)
        assert sum(model.current_position.values()) == -400

        # すべて精算
        model.buy_all_if_possible(target_date)
        model.margin(target_date) == 1000000
        assert sum(model.current_position.values()) == 0
