
import datetime
from typing import Dict, List, Optional

import polars as pl

from .. import const
from .statements_report import StatementsReport


class StatementsHistory:

    """ ある銘柄の過去の決算発表をまとめて管理するクラス
    """

    def __init__(self, df: pl.DataFrame):
        self._df = df

        # 日付でソート
        self._df = self._df.with_columns(
            pl.col(const.STATEMENTS_DATE).str.strptime(pl.Date, fmt="%Y-%m-%d"),
            pl.col(const.STATEMENTS_FISCAL_YEAR_START).str.strptime(pl.Date, fmt="%Y-%m-%d"),
            pl.col(const.STATEMENTS_FISCAL_YEAR_END).str.strptime(pl.Date, fmt="%Y-%m-%d")
        )
        self._df = self._df.sort(const.STATEMENTS_DATE)

        # 関係の無い報告を弾く
        def report_filter(series: pl.Expr) -> pl.Expr:
            is_other = series.str.starts_with("OtherPeriodFinancialStatements")
            is_numeric_correction = series.str.starts_with("NumericalCorrection")
            is_forecast_revision = series.str.starts_with("ForecastRevision")
            return ~(is_other | is_numeric_correction | is_forecast_revision)
        self._df = self._df.filter(report_filter(pl.col("TypeOfDocument")))

        # 欠損値を補完する
        self._df = complete_numerical_correction(self._df)

        if len(self._df) == 0:
            raise ValueError("DataFrame has no records .")

        # 特徴量
        self.company_name = str(self._df[-1, "CompanyName"])
        self.stock_code = str(self._df[-1, "LocalCode"]).zfill(5)

        self.cache: Dict[str, StatementsReport] = {}

    def list_reports(self) -> List[StatementsReport]:
        report_ls = []
        for i in range(len(self._df)):
            row = self._df[i]
            report = self.__row_to_report(row)
            report_ls.append(report)
        return report_ls

    def latest_report(self, date: datetime.date, periods: int = 1) -> Optional[StatementsReport]:
        """ 指定した日付時点での最新の決算報告書を取得する　
        """
        df = self._df.filter(pl.col(const.STATEMENTS_DATE) < date)
        if len(df) < periods:
            return None
        latest = df[-periods]

        # hashを確認して既にオブジェクトを生成していたらそれを返す
        hash = latest[0, const.STATEMENTS_HASH]
        if hash in self.cache:
            return self.cache[hash]
        report = StatementsReport(latest)
        self.cache[hash] = report
        return report

    def previous_quarter(self, base_report: StatementsReport, n: int) -> Optional[StatementsReport]:
        """ 指定された決算のN期前の決算を返す
        """
        # 指定された決算より前の決算を列挙する
        date = base_report.disclosed_date
        df = self._df.filter(pl.col(const.STATEMENTS_DATE) <= date)
        yq = base_report._year_quarter.previous_quarter(n)

        for i in range(len(df)):
            idx = -1 * (i + 1)
            report = self.__row_to_report(df[idx])
            if report._year_quarter == yq:
                return report
        return None

    def previous_year(self, base_report: StatementsReport, n: int) -> Optional[StatementsReport]:
        # 指定された決算より前の決算を列挙する
        date = base_report.disclosed_date
        df = self._df.filter(pl.col(const.STATEMENTS_DATE) <= date)
        yq = base_report._year_quarter.previous_year(n)

        for i in range(len(df)):
            idx = -1 * (i + 1)
            report = self.__row_to_report(df[idx])
            if report._year_quarter == yq:
                return report
        return None

    def __row_to_report(self, row: pl.DataFrame) -> StatementsReport:
        """ pl.DataFrameをStatementsReportに変換する
        """
        if len(row) != 1:
            raise ValueError("Argument row must be 1 length dataframe.")
        hash = row[0, const.STATEMENTS_HASH]
        if hash in self.cache:
            return self.cache[hash]
        report = StatementsReport(row)
        self.cache[hash] = report
        return report


def complete_numerical_correction(df: pl.DataFrame) -> pl.DataFrame:
    """ 予想修正や数値修正の欠損を前回発表値から補正する

    Note:
    厳密にはDisclosedDateが同じ決算を見つけて修正するべきだがソートしてあるのでおおよそ同じ挙動となる
    (訂正時にはDisclosedDateを書き換えずに公表される.)
    """
    # 補正の対象となるTypeOfDocument
    target_type = [
        "ForecastRevision",
        "NumericalCorrection"
    ]

    # 特定の列は欠損値にした上で、前回報告分をコピーする
    blank_and_fill = [
        "TypeOfCurrentPeriod"
    ]
    for col in blank_and_fill:
        df = df.with_columns(
            pl.when(pl.col("TypeOfDocument").is_in(target_type))
            .then(None)
            .otherwise(pl.col(col)).alias(col)
        )

    # 前1つ分の数字を見て補完処理をする
    ignore_list = ["TypeOfDocument"]
    all_columns = df.columns
    for col in all_columns:
        if col in ignore_list:
            continue
        df = df.with_columns(
            pl.when(pl.col("TypeOfDocument").is_in(target_type))
            .then(pl.col(col).fill_null(strategy="forward", limit=1))
            .otherwise(pl.col(col))
        )

    # TypeOfCurrentPeriodが定義されていないレコードは除く
    # 現状2連続で訂正が入った場合に生じうる
    allowed_period = ["FY", "1Q", "2Q", "3Q"]
    df = df.filter(pl.col("TypeOfCurrentPeriod").is_in(allowed_period))
    return df
