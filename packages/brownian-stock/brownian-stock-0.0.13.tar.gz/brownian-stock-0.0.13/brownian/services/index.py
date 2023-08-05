

import polars as pl

from .. import const
from ..models.index_series import IndexSeries
from ..models.stock_set import StockSet


def turnover_weighted_index(stock_set: StockSet):
    """ 最終日の出来高で各株価を重み付けした指標
    """
    brand_dict = {}
    for s in stock_set:
        series = s.to_series(const.COL_CLOSE)
        brand_dict[s.stock_code] = series

    df = pl.DataFrame(brand_dict)
    df = df.drop_nulls()
    brand_list = list(df.columns)

    # 最終日の出来高で重み付け平均
    weight = 0 
    for s in stock_set:
        code = s.stock_code
        if code not in brand_list:
            continue
        volume = s.latest_value(const.COL_TRADING_VOLUME)
        df[code] *= volume
        weight += volume
    df.with_columns(
        pl.fold(0, lambda acc, s: acc + s, pl.all())
    )

    normalized = df.sum(axis=1) / weight
    normalized.name = "IndexValue"
    normalized = normalized.reset_index()
    index_series = IndexSeries(normalized)
    return index_series


def average_index(stock_set: StockSet, column:str = const.COL_CLOSE) -> IndexSeries:
    """ 最終日の出来高で各株価を重み付けした指標
    """
    df_ls = []
    brand_list = []
    for s in stock_set:
        brand_list.append(s.stock_code)
        df = s.dataframe(as_polars=True).select([pl.col(const.COL_DATE), pl.col(column)]).rename({column: s.stock_code})
        df_ls.append(df)

    df = df_ls.pop()
    while len(df_ls) > 0:
        pop_df = df_ls.pop()
        df = df.join(pop_df, on=const.COL_DATE, how="outer")

    # 空白を持つ場合にはdropする
    columns = df.columns
    for col in columns:
        if col == const.COL_DATE:
            continue
        count = df[col].null_count()
        if count > 0:
            df = df.drop(col)

    size = len(brand_list)
    df = df.with_columns(
        df.select(pl.all().exclude(const.COL_DATE))
          .fold(lambda acc, s: acc + s).alias("__SUM")
          .apply(lambda x: x / size)
    )
    index_series = IndexSeries(df[const.COL_DATE].to_list(), df["__SUM"].to_list())
    return index_series
