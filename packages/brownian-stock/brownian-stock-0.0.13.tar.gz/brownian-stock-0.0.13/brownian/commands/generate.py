
import datetime
import logging
import pathlib

import pandas as pd

from brownian.repository import (RawBrandRepository, RawStatementsRepository,
                                 RawStockRepository, RepositoryPath,
                                 StatementsCSVRepository,
                                 StatementsSQLRepository, StockCSVRepository,
                                 StockSQLRepository)

TABLE_PRICES = "prices"
TABLE_STATEMENTS = "statements"


def run_generate(dir_path: str, generate_all: bool, only_csv: bool, only_sql: bool):
    logger = logging.getLogger("__name__")

    # 引数の解析
    if only_csv and only_sql:
        raise ValueError("Either only_csv or only_sql can use.")
    run_sql_actions = not only_csv
    run_csv_actions = not only_sql

    repository_path = RepositoryPath(dir_path)
    repository_path.setup_dir()
    if run_sql_actions:
        insert_brand_csv(repository_path, logger)
        insert_stock_csv(repository_path, logger)
        insert_statements_csv(repository_path, logger, skip_past=not generate_all)
    if run_csv_actions:
        create_statements_csv(repository_path, logger)
        create_stock_csv(repository_path, logger)


def insert_stock_csv(repository_path: RepositoryPath, logger: logging.Logger) -> None:
    """ 保存した株価のCSVをDBに挿入していく
    """
    stock_repo = RawStockRepository(repository_path)
    if not stock_repo.table_exists():
        stock_repo.create_table()

    logger.info("Start to drop the index on stock table.")
    stock_repo.drop_index()
    logger.info("Complete to drop the index on stock table.")

    existing_date = stock_repo.existing_date()

    file_list = list(sorted(repository_path.raw_stock_path.iterdir()))
    for csv_path in file_list:
        if csv_path.is_dir():
            logger.error(f"{csv_path.name} is not file.")
            continue
        # ファイル名から日付を読み込む
        date_str = csv_path.name.replace(".csv", "")
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            logger.error(f"Failed to parse date from filename. Filename is {csv_path.name}.")
            continue

        if date in existing_date:
            logger.info(f"Records already exists. Skip insert {csv_path.name}.")
            continue

        # j# 過去のファイルだった場合には処理をスキップ
        # if skip_past and date < datetime.date.today():
        #     continue

        # 既に存在していた場合には処理をスキップ
        # if stock_repo.has_records(date):
        #     logger.info(f"Records already exists. Skip insert {csv_path.name}.")
            # continue
        df = pd.read_csv(csv_path, index_col=0)
        df["Date"] = pd.to_datetime(df["Date"])
        try:
            stock_repo.insert_daily_df(df)
            logger.info(f"Success to insert {csv_path.name}.")
        except Exception:
            logger.error(f"Error occurred until inserting {csv_path.name}.")

    logger.info("Start setting the index on stock table.")
    stock_repo.set_index()
    logger.info("Complete setting the index on stock table.")

    size = stock_repo.records_size()
    logger.info("Complete to insert stock price csv.")
    logger.info(f"Total Record Size: {size}")


def insert_statements_csv(repository_path: RepositoryPath, logger: logging.Logger, skip_past=True):
    statements_repo = RawStatementsRepository(repository_path)
    if not statements_repo.table_exists():
        statements_repo.create_table()

    logger.info("Start to drop the index on statements table.")
    statements_repo.drop_index()
    logger.info("Complete to drop the index on statements table.")

    file_list = list(sorted(repository_path.raw_statements_path.iterdir()))
    for csv_path in file_list:
        if csv_path.is_dir():
            logger.error(f"{csv_path.name} is not file.")
            continue

        # ファイル名から日付を読み込む
        date_str = csv_path.name.replace(".csv", "")
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            logger.error(f"Failed to parse date from filename. Filename is {csv_path.name}.")
            continue

        # 既に存在していた場合には処理をスキップ
        if statements_repo.has_records(date):
            logger.info(f"Records already exists. Skip insert {csv_path.name}.")
            continue

        # 決算情報は対象日に公開されたデータが無い場合がある
        if csv_path.stat().st_size == 0:
            logger.info(f"No records in {csv_path.name}.")
            continue

        # CSVを読み込んでInsert
        df = pd.read_csv(csv_path, index_col=0)
        df["DisclosedDate"] = pd.to_datetime(df["DisclosedDate"])
        try:
            statements_repo.insert_statements_df(df)
            logger.info(f"Success to insert {csv_path.name}.")
        except Exception:
            logger.error(f"Error occurred until inserting {csv_path.name}.")

    logger.info("Start setting the index on statements table.")
    statements_repo.set_index()
    logger.info("Complete setting the index on statements table.")

    size = statements_repo.records_size()
    logger.info("Complete to insert statements price csv.")
    logger.info(f"Total Record Size: {size}")


def insert_brand_csv(repository_path: RepositoryPath, logger: logging.Logger) -> None:
    """ ダウンロードした銘柄一覧をデータベースに格納する
    """
    brand_repo = RawBrandRepository(repository_path)
    if not brand_repo.table_exists():
        brand_repo.create_table()

    csv_path = repository_path.brand_path
    df = pd.read_csv(csv_path, index_col=0)
    df["Date"] = pd.to_datetime(df["Date"])
    brand_repo.insert_brand_df(df)

    size = brand_repo.records_size()
    logger.info("Complete to insert brand csv.")
    logger.info(f"Total Record Size: {size}")


def create_stock_csv(repository_path: RepositoryPath, logger: logging.Logger) -> None:
    """ Databaseに格納した情報を集計して個別銘柄のCSVとして吐き出す
    """
    logger.info("Loading stock set from sqlite database.")
    sql_repo = StockSQLRepository(repository_path)
    logger.info("Generating stock csv.")
    csv_repo = StockCSVRepository(repository_path)
    stock_set = sql_repo.load()
    csv_repo.save(stock_set)


def create_statements_csv(repository_path: RepositoryPath, logger: logging.Logger) -> None:
    """ Databaseに格納した情報を集計して個別銘柄のCSVとして吐き出す
    """
    # レポジトリの初期化
    logger.info("Loading stock set from sqlite database.")
    sql_repo = StatementsSQLRepository(repository_path)
    logger.info("Generating statements csv.")
    csv_repo = StatementsCSVRepository(repository_path)

    # 処理の実行
    stock_set = sql_repo.load()
    csv_repo.save(stock_set)


def insert_statement(conn, dir_path: str) -> None:
    raw_statements_dir = pathlib.Path(dir_path) / "raw_statements"

    for csv_name in raw_statements_dir.iterdir():
        try:
            print(csv_name)
            df = pd.read_csv(csv_name)
            df.to_sql(TABLE_STATEMENTS, conn, if_exists="append", index=False)
        except Exception as e:
            print(e)
            print("Error")
