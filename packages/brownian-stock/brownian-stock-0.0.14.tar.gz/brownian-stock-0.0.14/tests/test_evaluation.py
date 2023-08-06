
import datetime
import pathlib

import pytest
from brownian import evaluation, load_stock_series


def test_percentage_change():

    filepath = pathlib.Path(__file__).parent / "data" / "stock_86970.csv"
    stock_series = load_stock_series(filepath)


    start_date = datetime.date(2022, 4, 1)
    end_date = datetime.date(2022, 4, 8)
    subset = stock_series.subset_by_range(start_date, end_date)

    eval_obj = evaluation.PercentageChangeStockEval()
    rate = eval_obj(subset)
    assert rate == pytest.approx(0.9923, 0.001)