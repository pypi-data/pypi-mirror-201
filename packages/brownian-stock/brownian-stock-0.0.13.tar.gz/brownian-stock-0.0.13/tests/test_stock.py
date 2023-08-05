

import datetime
import pathlib

import pytest

import brownian
from brownian import const


def test_subset_by_range() -> None:
    """ subset_by_rangeメソッドの動作検証
    """
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = brownian.load_stock_series(filepath)

    # 2022/04のsubsetを抽出して日数が20日であることを確認する
    start_date = datetime.date(2022, 4, 1)
    end_date = datetime.date(2022, 4, 30)
    subset = stock_series.subset_by_range(start_date, end_date)
    assert subset.size() == 20

    # subsetの最初の日が2022/04/01であること
    min_date = subset.dataframe()[const.COL_DATE].min()
    assert min_date.date() == datetime.date(2022, 4, 1)

    # subsetの最後の日が2022/04/30であること
    max_date = subset.dataframe()[const.COL_DATE].max()
    assert max_date.date() == datetime.date(2022, 4, 28)


def test_subset_recent_n_days() -> None:
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = brownian.load_stock_series(filepath)

    # 2022/04のsubsetを抽出して日数が20日であることを確認する
    start_date = datetime.date(2022, 4, 1)
    subset = stock_series.subset_by_recent_n_days(start_date, 20)
    assert subset.size() == 20

    # subsetの最後の日が2022/04/30であること
    max_date = subset.dataframe()[const.COL_DATE].max()
    assert max_date.date() == datetime.date(2022, 3, 31)

    # Case2. 異常系
    # n_days分のデータが取れない場合にValueErrorが発生すること
    start_date = datetime.date(2017, 1, 10)
    with pytest.raises(ValueError):
        subset = stock_series.subset_by_recent_n_days(start_date, 30)

    # to_arrayを使ってすべての要素が一致することを確認
    start_date = datetime.date(2022, 4, 1)
    a1 = stock_series.subset_by_recent_n_days(start_date, 20).to_array(const.COL_CLOSE)
    a2 = stock_series.subset_by_recent_n_days(start_date, 30).to_array(const.COL_CLOSE)
    assert (a1[-20:] == a2[-20:]).all()


def test_subset_after_n_days() -> None:
    """ StockSeriesのtest_subset_fater_n_days()のテスト
    """
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = brownian.load_stock_series(filepath)

    # Case1. 正常系
    # 2022/04のsubsetを抽出して日数が20日であることを確認する
    start_date = datetime.date(2022, 4, 1)
    subset = stock_series.subset_by_after_n_days(start_date, 20)
    assert subset.size() == 20
    # subsetの最初の日が2022/04/01であること
    min_date = subset.dataframe()[const.COL_DATE].min()
    assert min_date.date() == datetime.date(2022, 4, 1)
    # subsetの最後の日が2022/04/30であること
    max_date = subset.dataframe()[const.COL_DATE].max()
    assert max_date.date() == datetime.date(2022, 4, 28)

    # Case2. 異常系
    # n_days分のデータが取れない場合にValueErrorが発生すること
    start_date = datetime.date(2023, 2, 19)
    with pytest.raises(ValueError):
        subset = stock_series.subset_by_after_n_days(start_date, 30)


def test_stock_set() -> None:
    """ StockSetのテスト
    """
    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = brownian.load_stock_series(filepath)
    stock_ls = [stock_series]

    # get_stockの動作の確認
    stock_set = brownian.StockSet(stock_ls)
    stock = stock_set.get_stock("86970")
    assert stock == stock_series

    # lenが機能するか
    assert len(stock_set) == 1

    # iterが使えるか
    for _ in stock_set:
        pass

    # subset周りの関数群の簡単な評価
    one_subset = stock_set.subset_by_available_at(datetime.date(2022, 4, 1))
    assert len(one_subset) == 1

    zero_subset = stock_set.subset_by_available_at(datetime.date(2022, 4, 2))
    assert len(zero_subset) == 0

    # 境界条件
    one_subset = stock_set.subset_by_available_at(datetime.date(2023, 2, 17))
    assert len(one_subset) == 1

    one_subset = stock_set.subset_by_available_at(datetime.date(2023, 2, 17))
    assert len(one_subset) == 1


