
import datetime
import sqlite3

import pandas as pd

from .repository_path import RepositoryPath

TABLE_STATEMENTS = "statements"


class RawStatementsRepository:

    """ ダウンロードした生の決算情報をデータベースに挿入するためのレポジトリ
    """

    def __init__(self, repository_path: RepositoryPath):
        self.repository_path = repository_path

    def insert_statements_df(self, df: pd.DataFrame) -> None:
        """ データベースに対象日のレコードを挿入する
        """

        # 入力のチェック
        if len(df) == 0:
            raise ValueError("DataFrame is empty.")

        if len(df["DisclosedDate"].unique()) != 1:
            raise ValueError("DataFrame contains two or more different disclosed date.")

        # 既にレコードが存在していたら一度削除する
        conn = self.__get_connection()
        date = df["DisclosedDate"][0]
        if self.has_records(date):
            date_str = date.strftime("%Y-%m-%d")
            conn.execute(f"DELETE FROM stock WHERE DisclosedDateDate='{date_str}'")

        # 挿入処理
        df = preprocess_before_insert(df)
        df.to_sql(TABLE_STATEMENTS, conn, if_exists="append", index=False)
        conn.close()

    def drop_index(self) -> None:
        """ Indexを落とす
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("DROP INDEX IF EXISTS statements_index;")
        conn.commit()
        conn.close()

    def set_index(self) -> None:
        """ CodeにIndexを貼る
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS statements_index ON statements (LocalCode);")
        conn.commit()
        conn.close()

    def create_table(self) -> None:
        """ 新しくstockテーブルを生成する
        """
        conn = self.__get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE statements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            DisclosureNumber TEXT,
            DisclosedDate TEXT,
            ApplyingOfSpecificAccountingOfTheQuarterlyFinancialStatements TEXT,
            AverageNumberOfShares REAL,
            BookValuePerShare REAL,
            ChangesBasedOnRevisionsOfAccountingStandard TEXT,
            ChangesInAccountingEstimates TEXT,
            ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard TEXT,
            CurrentFiscalYearEndDate TEXT,
            CurrentFiscalYearStartDate TEXT,
            CurrentPeriodEndDate TEXT,
            DisclosedTime TEXT,
            DisclosedUnixTime TEXT,
            EarningsPerShare TEXT,
            Equity REAL,
            EquityToAssetRatio REAL,
            ForecastDividendPerShare1stQuarter REAL,
            ForecastDividendPerShare2ndQuarter REAL,
            ForecastDividendPerShare3rdQuarter REAL,
            ForecastDividendPerShareAnnual REAL,
            ForecastDividendPerShareFiscalYearEnd REAL,
            ForecastEarningsPerShare REAL,
            ForecastNetSales REAL,
            ForecastOperatingProfit REAL,
            ForecastOrdinaryProfit REAL,
            ForecastProfit REAL,
            LocalCode TEXT,
            MaterialChangesInSubsidiaries TEXT,
            NetSales REAL,
            NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock REAL,
            NumberOfTreasuryStockAtTheEndOfFiscalYear REAL,
            OperatingProfit REAL,
            OrdinaryProfit REAL,
            Profit REAL,
            ResultDividendPerShare1stQuarter REAL,
            ResultDividendPerShare2ndQuarter REAL,
            ResultDividendPerShare3rdQuarter REAL,
            ResultDividendPerShareAnnual REAL,
            ResultDividendPerShareFiscalYearEnd REAL,
            RetrospectiveRestatement TEXT,
            TotalAssets TEXT,
            TypeOfCurrentPeriod TEXT,
            TypeOfDocument TEXT
        );""")

        conn.commit()
        conn.close()

    def table_exists(self) -> bool:
        """ priceテーブルが存在するか判定する
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='statements';")
        size = res.fetchone()
        is_exist :bool = size[0] > 0
        conn.commit()
        conn.close()
        return is_exist

    def has_records(self, date: datetime.date) -> bool:
        """ 対象日のデータが存在するか確認する
        """
        if not isinstance(date, datetime.date):
            raise TypeError("date must be 'datetiem.date'")
        date_str = date.strftime("%Y-%m-%d")
        conn = self.__get_connection()
        res = conn.execute(f"SELECT COUNT(*) FROM statements WHERE DisclosedDate='{date_str}';")
        size = res.fetchone()
        is_exist :bool = size[0] > 0
        conn.close()
        return is_exist

    def records_size(self) -> int:
        """ データ総数を取得
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM statements;")
        size :int = res.fetchone()[0]
        conn.commit()
        conn.close()
        return size

    def __get_connection(self) -> sqlite3.Connection:
        db_path = self.repository_path.sqlite_path
        conn = sqlite3.connect(db_path)
        return conn


def preprocess_before_insert(df: pd.DataFrame) -> pd.DataFrame:
    """ Unicode型をSqliteが扱えないので予め処理する
    """
    df = df.replace("－", None)
    df["DisclosedDate"] = df["DisclosedDate"].dt.strftime("%Y-%m-%d")
    return df
