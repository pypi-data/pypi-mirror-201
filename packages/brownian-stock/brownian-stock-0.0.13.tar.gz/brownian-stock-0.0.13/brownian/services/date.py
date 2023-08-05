

import datetime
from typing import Optional

import polars as pl

from .. import const
from ..repository import RepositoryPath


def market_open_dates(repository_path: RepositoryPath, start_date:Optional[datetime.date] = None,
                      end_date: Optional[datetime.date] = None):
    """ 市場が開場している日のリストを返す
    """
    conn = "sqlite://" + str(repository_path.sqlite_path.absolute())

    days_df = pl.read_sql("SELECT DISTINCT(Date) FROM stock ORDER BY Date;", conn)
    days_df = days_df.with_columns(pl.col(const.COL_DATE).str.strptime(pl.Date, fmt="%Y-%m-%d"))
    days = days_df[const.COL_DATE].to_list()

    if start_date:
        days = filter(lambda d: d >= start_date, days)
    if end_date:
        days = filter(lambda d: d <= end_date, days)
    days = list(days)
    return days
