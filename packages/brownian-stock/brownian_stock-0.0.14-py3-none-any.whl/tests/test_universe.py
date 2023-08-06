
import pathlib

import brownian
from brownian.services import universe


def load_stock(code):
    """ ダミーの株価を読み込むための補助関数
    """
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    s = brownian.load_stock_series(filepath)
    s.stock_code = code
    return s


def test_core30():
    univ = universe.TopixCore30()

    # 72030 トヨタ自動車はCore30の銘柄
    assert univ(load_stock("72030"))

    # 41880 三菱ケミカルはLarge70の銘柄
    assert not univ(load_stock("41880"))

    # 47160 日本造船はMid400の銘柄
    assert not univ(load_stock("47160"))

    # 70140 名村造船はSmall1の銘柄
    assert not univ(load_stock("70140"))

    # 43190 TACはSmall2の銘柄
    assert not univ(load_stock("43190"))


def test_large70():
    univ = universe.TopixLarge70()

    # 41880 三菱ケミカルはLarge70の銘柄
    assert univ(load_stock("41880"))

    # 72030 トヨタ自動車はCore30の銘柄
    assert not univ(load_stock("72030"))

    # 47160 日本造船はMid400の銘柄
    assert not univ(load_stock("47160"))

    # 70140 名村造船はSmall1の銘柄
    assert not univ(load_stock("70140"))

    # 43190 TACはSmall2の銘柄
    assert not univ(load_stock("43190"))


def test_mid400():
    univ = universe.TopixMid400()

    # 47160 日本造船はMid400の銘柄
    assert univ(load_stock("47160"))

    # 72030 トヨタ自動車はCore30の銘柄
    assert not univ(load_stock("72030"))

    # 41880 三菱ケミカルはLarge70の銘柄
    assert not univ(load_stock("41880"))

    # 70140 名村造船はSmall1の銘柄
    assert not univ(load_stock("70140"))

    # 43190 TACはSmall2の銘柄
    assert not univ(load_stock("43190"))


def test_topix_small_1():
    univ = universe.TopixSmall1()

    # 70140 名村造船はSmall1の銘柄
    assert univ(load_stock("70140"))

    # 72030 トヨタ自動車はCore30の銘柄
    assert not univ(load_stock("72030"))

    # 41880 三菱ケミカルはLarge70の銘柄
    assert not univ(load_stock("41880"))

    # 47160 日本造船はMid400の銘柄
    assert not univ(load_stock("47160"))

    # 43190 TACはSmall2の銘柄
    assert not univ(load_stock("43190"))


def test_topix_small_2():
    univ = universe.TopixSmall2()

    # 43190 TACはSmall2の銘柄
    assert univ(load_stock("43190"))

    # 72030 トヨタ自動車はCore30の銘柄
    assert not univ(load_stock("72030"))

    # 41880 三菱ケミカルはLarge70の銘柄
    assert not univ(load_stock("41880"))

    # 47160 日本造船はMid400の銘柄
    assert not univ(load_stock("47160"))

    # 70140 名村造船はSmall1の銘柄
    assert not univ(load_stock("70140"))
