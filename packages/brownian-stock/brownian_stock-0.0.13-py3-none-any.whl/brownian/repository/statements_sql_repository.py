
from typing import List

import polars as pl
import tqdm

from ..models.statements import StatementsHistory
from .repository_path import RepositoryPath


class StatementsSQLRepository:

    def __init__(self, repository_path: RepositoryPath):
        self.repository_path = repository_path

    def load(self, limit=None) -> List[StatementsHistory]:
        statements_list = []
        failed_list = []

        conn = self.__get_connection()
        brand_df = pl.read_sql("SELECT Code FROM brand;", conn)
        brand_list = brand_df["Code"].unique().to_list()

        for brand in tqdm.tqdm(brand_list):
            try:
                df = load_statements(conn, brand)
                if df is None:
                    continue
                statements = StatementsHistory(df)
                statements_list.append(statements)
            except Exception:
                failed_list.append(brand)
        for brand in failed_list:
            self.log(f"[*] Failed to load {brand}")
        return statements_list

    def __get_connection(self) -> str:
        """ Sqlite用のConnectionStringを生成する
        https://sfu-db.github.io/connector-x/databases/sqlite.html
        """
        conn = "sqlite://" + str(self.repository_path.sqlite_path.absolute())
        return conn

    def log(self, msg):
        print(msg)


def load_statements(conn: str, brand: str):
    """ DBから決算情報を読み込む
    """
    query = f"""
        SELECT *
        FROM statements
        JOIN brand ON statements.LocalCode = brand.Code
        WHERE statements.LocalCode = '{brand}';
    """
    df = pl.read_sql(query, conn)
    if len(df) == 0:
        return None
    return df
