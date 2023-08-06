
from __future__ import annotations

import datetime
import logging
from typing import Any, Optional

import polars as pl
from dateutil.relativedelta import relativedelta

from .. import const
from ..models.stock_series import StockSeries

logger = logging.getLogger(__name__)


class YearQuarter:

    """ 日付管理用クラス.
    内部での利用に限定して, パッケージ外には公開しない
    """

    quarter_dict = {
        "1Q": 0,
        "2Q": 1,
        "3Q": 2,
        "FY": 3
    }

    @classmethod
    def quarter_int_to_str(cls, quarter: int) -> str:
        reversed_dict = {v: k for k, v in cls.quarter_dict.items()}
        return reversed_dict[quarter]

    @classmethod
    def quarter_str_to_int(cls, quarter: str) -> int:
        return cls.quarter_dict[quarter]

    def __init__(self, year: int, quarter: str) -> None:
        logger.debug(f"YearQuarter init by ({year}-{quarter})")
        self.year = year
        self.quarter = self.quarter_str_to_int(quarter)

    def __repr__(self) -> str:
        q = self.quarter_int_to_str(self.quarter)
        return f"{self.year}-{q}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, YearQuarter):
            raise TypeError(f"Can't compare YearQuarter with {type(other)} ")
        return self.year == other.year and self.quarter == other.quarter

    def previous_quarter(self, n: int) -> YearQuarter:
        """ 指定した決算のn期前の決算を取得する
        """
        previous_quarter = self.quarter - n

        y = previous_quarter // 4
        q = (previous_quarter + abs(n) * 4) % 4

        str_quarter = self.quarter_int_to_str(q)
        return YearQuarter(self.year + y, str_quarter)

    def previous_year(self, n: int) -> YearQuarter:
        """ 指定した決算のn年前の決算を取得する
        """
        str_quarter = self.quarter_int_to_str(self.quarter)
        return YearQuarter(self.year - n, str_quarter)


class StatementsReport:

    def __init__(self, row: pl.DataFrame):
        if len(row) != 1:
            raise ValueError("Row length must be 1.")
        self._row = row

        self.hash = row[0, const.STATEMENTS_HASH]
        # 管理しやすようにプロパティとして主要なものを定義
        self.company_name = row[0, const.STATEMENTS_COMPANY_NAME]
        self.stock_code = row[0, const.STATEMENTS_STOCK_CODE]

        self.disclosed_date :datetime.date = row[0, const.STATEMENTS_DATE]
        self.fiscal_year_start :datetime.date = row[0, const.STATEMENTS_FISCAL_YEAR_START]
        self.fiscal_year_end :datetime.date = row[0, const.STATEMENTS_FISCAL_YEAR_END]
        self.type_of_document :str = row[0, const.STATEMENTS_TYPE_OF_DOCUMENT]

        self.stock_number = row[0, const.STATEMENTS_STOCK_NUM]  # 期末における株式数
        self.treasury_stock_number = row[0, const.STATEMENTS_TREASURY_STOCK_NUM]  # 期末における株式数
        self.assets = row[0, const.STATEMENTS_ASSETS]  # 総資産
        # self.dividend_forecast = row[0, const.STATEMENTS_DVIDEND_FORECAST]  # 配当予想

        # 日次に関する情報
        # StatementsHistory以外からは参照しない
        year = self.fiscal_year_start.year
        quarter = row[0, const.STATEMENTS_QUARTER]
        self._year_quarter = YearQuarter(year, quarter)
        logger.debug(f"StatementsReport({self.company_name}, {self.disclosed_date}) inited.")

    def __repr__(self) -> str:
        return f"[{self.stock_code}]{self.company_name}: {self._year_quarter}"

    def show(self) -> None:
        print(self._row.melt())

    def current_quarter(self, d: datetime.date) -> Optional[int]:
        """ このレポートに記載されている事業年度を元に, 指定した日が何Qかを返す

        Args:
            d(datetime.date)

        Returns:
            int: 1Q->0, 2Q->1, 3Q->2, FY->3
        """

        current_quarter = 0
        month = d.month

        # 特殊ケース: 2/29の場合は3/1とみなして計算を簡単にする
        fiscal_year_start = self.fiscal_year_start
        if fiscal_year_start.month == 2 and fiscal_year_start.day == 29:
            fiscal_year_start += datetime.timedelta(days=1)
        if fiscal_year_start.day != 1:
            logger.warning(f"FiscalYearStart doesn't start with 1st. {fiscal_year_start}, {self.company_name}")
            return None
        start_month = self.fiscal_year_start.month

        for i in range(12):
            m = (start_month + i - 1) % 12 + 1
            if m == month:
                return current_quarter
            if (i + 1) % 3 == 0:
                current_quarter += 1
        raise RuntimeError("Program can't reach here. Something wrong.")

    def recent_quarter_end(self, target_date: datetime.date) -> datetime.date:
        """ 指定した日から最も近い未来の期末日を返す
        """
        # 特殊ケース: 2/29の場合は3/1とみなして計算を簡単にする
        fiscal_year_start = self.fiscal_year_start
        if fiscal_year_start.month == 2 and fiscal_year_start.day == 29:
            fiscal_year_start += datetime.timedelta(days=1)
        if fiscal_year_start.day != 1:
            logger.warning(f"FiscalYearStart doesn't start with 1st. {fiscal_year_start}, {self.company_name}")
        start_month = self.fiscal_year_start.month

        # 期末のリストを返す
        base_month = (start_month + 1) % 12 + 1  # 期首を期末に変換している
        quarter_end_list = []
        for i in range(4):
            month = base_month + i * 3
            month = (month - 1) % 12 + 1
            quarter_end_list.append(month)

        # 月初めにする
        target_date = target_date + relativedelta(day=1)
        for i in range(12):
            d = target_date + relativedelta(months=i)
            if d.month in quarter_end_list:
                # 月末の日を返す
                return d + relativedelta(months=1, day=1, days=-1)
        raise RuntimeError("Program can't reach here. Something wrong.")

    @property
    def year(self) -> int:
        return self._year_quarter.year

    @property
    def quarter(self) -> int:
        return self._year_quarter.quarter

    @property
    def type_of_document_period(self) -> int:
        return self._year_quarter.quarter

    def dividend_forecast(self, quarter_idx: int) -> Optional[float]:
        """ 各期末の予想配当
        """
        key_dict = {
            0: const.STATEMENTS_DIVIDEND_FORECAST_1Q,
            1: const.STATEMENTS_DIVIDEND_FORECAST_2Q,
            2: const.STATEMENTS_DIVIDEND_FORECAST_3Q,
            3: const.STATEMENTS_DIVIDEND_FORECAST_4Q
        }
        key = key_dict.get(quarter_idx)
        if key is None:
            return None
        value = self._row[0, key]
        if value is None:
            return 0
        return float(value)

    @property
    def dividend_forecast_total(self) -> Optional[float]:
        """ 一年を通じた予想配当の合計
        """
        dividend = self._row[0, const.STATEMENTS_DVIDEND_FORECAST]  # 配当予想
        if dividend is None:
            return 0
        return float(dividend)

    def dividend_result(self, quarter_idx: int) -> Optional[float]:
        key_dict = {
            0: const.STATEMENTS_DIVIDEND_RESULT_1Q,
            1: const.STATEMENTS_DIVIDEND_RESULT_2Q,
            2: const.STATEMENTS_DIVIDEND_RESULT_3Q,
            3: const.STATEMENTS_DIVIDEND_RESULT_4Q,
        }
        key = key_dict.get(quarter_idx)
        if key is None:
            return None
        value = self._row[0, key]
        if value is None:
            return 0
        return float(value)

    @property
    def dividend_result_total(self) -> Optional[float]:
        """ 一年を通じた配当実績の合計
        """
        dividend = self._row[0, const.STATEMENTS_DIVIDEND_RESULT]  # 配当予想
        if dividend is None:
            return 0
        return float(dividend)

    def price_at_disclosure(self, stock_series: StockSeries) -> float:
        """ 決算高表示の株価を取得
        """
        disclosed_date = self.disclosed_date

        # 現在の株価を決算時の調整係数で修正する
        recent = stock_series.subset_by_recent_n_days(disclosed_date, 7)
        close_price = recent.latest_value(const.COL_CLOSE)
        factor_at_disclose = recent.latest_value(const.COL_ADJUSTMENT_FACTOR)

        close_price_at_disclose: float = close_price * factor_at_disclose
        return close_price_at_disclose

    # 1株あたり純利益
    @property
    def eps(self) -> float:
        return float(self._row[0, "EarningsPerShare"])  # 1株あたり当期純利益

    # 当期純利益
    @property
    def profit(self) -> Optional[int]:
        """ 当期純利益
        """
        value = self._row[0, const.STATEMENTS_PROFIT]
        if value is None:
            return None
        return int(value)

    # 通年予想利益
    @property
    def forecast_profit(self) -> int:
        """ 通年利益予想
        """
        return int(self._row[0, const.STATEMENTS_FORECAST_PROFIT])  # 当期利益

    @property
    def net_sales(self) -> Optional[int]:
        """ 当期総売上高
        """
        value = self._row[0, const.STATEMENTS_NET_SALES]
        if value is None:
            return None
        return int(value)

    @property
    def forecast_net_sales(self) -> Optional[int]:
        """ 当期総売上高
        """
        value = self._row[0, const.STATEMENTS_FORECAST_NET_SALES]
        if value is None:
            return None
        return int(value)

    @property
    def equity(self) -> Optional[int]:
        """ 純資産
        """
        value = self._row[0, const.STATEMENTS_EQUITY]
        if value is None:
            return None
        return int(value)
