
import sqlite3

import pandas as pd

from .repository_path import RepositoryPath

TABLE_BRAND = "brand"


class RawBrandRepository:

    """ ダウンロードした生のCSVをデータベースに挿入するためのレポジトリ
    """

    def __init__(self, repository_path: RepositoryPath):
        self.repository_path = repository_path

    def insert_brand_df(self, df: pd.DataFrame) -> None:
        """ データベースに対象日のレコードを挿入する
        """

        # 入力のチェック
        if len(df) == 0:
            raise ValueError("DataFrame is empty.")

        # レコードを一度すべて削除して再挿入
        conn = self.__get_connection()
        conn.execute("DELETE FROM brand;")
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
        df.to_sql(TABLE_BRAND, conn, if_exists="append", index=False)
        conn.close()

    def drop_index(self) -> None:
        """ Indexを落とす
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("DROP INDEX IF EXISTS brand_index;")
        conn.commit()
        conn.close()

    def set_index(self) -> None:
        """ CodeにIndexを貼る
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS brand_index ON brand (Code);")
        conn.commit()
        conn.close()

    def create_table(self) -> None:
        """ 新しくstockテーブルを生成する
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE brand( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            Code TEXT, \
            Date TEXT, \
            CompanyName TEXT, \
            Sector17Code INT, \
            Sector17CodeName TEXT, \
            Sector33Code INT, \
            Sector33CodeName TEXT, \
            ScaleCategory TEXT, \
            MarketCode INT, \
            MarketCodeName TEXT \
        );")
        conn.commit()
        conn.close()

    def table_exists(self) -> bool:
        """ priceテーブルが存在するか判定する
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='brand';")
        size = res.fetchone()
        is_exist :bool = size[0] > 0
        conn.commit()
        conn.close()
        return is_exist

    def records_size(self) -> int:
        """ データ総数を取得
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM brand;")
        size :int = res.fetchone()[0]
        conn.commit()
        conn.close()
        return size

    def __get_connection(self) -> sqlite3.Connection:
        db_path = self.repository_path.sqlite_path
        conn = sqlite3.connect(db_path)
        return conn
