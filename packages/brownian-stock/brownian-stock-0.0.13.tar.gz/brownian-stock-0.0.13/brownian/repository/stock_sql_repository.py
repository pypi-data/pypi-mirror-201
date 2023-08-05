
import datetime
import re
import traceback
from typing import List, Optional

import polars as pl
import tqdm

from .. import const
from ..models.stock_series import StockSeries
from ..models.stock_set import StockSet
from .repository_path import RepositoryPath


class StockSQLRepository:

    def __init__(self, repository_path: RepositoryPath, debug: bool = False) -> None:
        self.debug = debug
        self.repository_path = repository_path

    def load(self, stock_code: Optional[List[str]] = None) -> StockSet:
        stock_series_list = []
        failed_list = []

        conn = self.__get_connection()
        query = self.__build_query(stock_code=stock_code)
        brand_df = pl.read_sql(query, conn)
        brand_list = brand_df["Code"].unique().to_list()

        for brand in tqdm.tqdm(brand_list):
            try:
                df = load_stock(conn, brand)
                stock_series = StockSeries(df)
                stock_series_list.append(stock_series)
            except Exception as e:
                self.print_error(e)
                failed_list.append(brand)
        for brand in failed_list:
            self.log(f"[*] Failed to load {brand}")
        stock_set = StockSet(stock_series_list)
        return stock_set

    def print_error(self, error: Exception) -> None:
        if self.debug:
            print(traceback.format_tb(error.__traceback__))

    def __build_query(self, stock_code: Optional[List[str]] = None) -> str:
        base_query = "SELECT Code FROM brand"
        optional_condition = []

        if stock_code is not None:
            code_ls = []
            for code in stock_code:
                code_ls.append(f"'{code}'")
            where_query = "Code IN ({})".format(",".join(code_ls))
            optional_condition.append(where_query)

        # 条件に応じてクエリを生成
        if len(optional_condition) == 0:
            return base_query

        query_ls = [
            base_query,
            "WHERE",
            *optional_condition
        ]
        return " ".join(query_ls)

    def __get_connection(self) -> str:
        """ Sqlite用のConnectionStringを生成する
        https://sfu-db.github.io/connector-x/databases/sqlite.html
        """
        conn = "sqlite://" + str(self.repository_path.sqlite_path.absolute())
        return conn

    def log(self, msg: str) -> None:
        print(msg)


def load_stock(conn: str, brand: str) -> pl.DataFrame:
    query = f"""
        SELECT
            CompanyName,
            Sector17Code,
            Sector33Code,
            ScaleCategory,
            MarketCode,
            stock.Date,
            stock.Code,
            Close,
            Open,
            High,
            Low,
            Volume,
            TurnoverValue,
            AdjustmentFactor
        FROM stock
        JOIN brand ON stock.Code = brand.Code
        WHERE stock.Code = '{brand}';
    """
    df = pl.read_sql(query, conn)
    if len(df) == 0:
        raise RuntimeError(f"Tried to extract stock price information for the {brand}, but there were no results.")
    df = apply_adjust_factor(df)
    return df


def is_code(code_str: str) -> bool:
    ok = re.match(r"^\d\d\d\d\d$", code_str)
    return ok is not None


def apply_adjust_factor(df: pl.DataFrame) -> pl.DataFrame:
    """ 調整係数で最新の株価を調整する
    """
    df = df.sort(const.COL_DATE)
    factor = df[const.COL_ADJUSTMENT_FACTOR].cumprod()
    factor /= factor[-1]
    df = df.with_columns(factor.alias(const.COL_ADJUSTMENT_FACTOR))

    cols = [
        const.COL_CLOSE,
        const.COL_OPEN,
        const.COL_HIGH,
        const.COL_LOW,
        const.COL_TRADING_VOLUME
    ]

    # 調整係数をかけて小数点第一位で四捨五入
    df = df.with_columns(
        pl.col(cols).cast(pl.Float32) / factor
    )
    df = df.with_columns(
        pl.col(cols).round(1)
    )
    df = df.filter(pl.col(const.COL_DATE) != datetime.date(2020, 10, 1))
    return df
