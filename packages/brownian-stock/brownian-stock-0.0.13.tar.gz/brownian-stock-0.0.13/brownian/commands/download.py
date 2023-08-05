

import datetime
import logging
import os
import time
import warnings
from typing import List, Optional

from ..models.calendar import Calendar
from ..repository import IndexCsvRepository, RepositoryPath
from ..services import jquants, yahoo
from ..services.dot_file import load_config

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def run_download(dir_path: str, limit: Optional[int] = None, only_stock: bool = False,
                 only_brand: bool = False, only_statments :bool = False,
                 only_yahoo :bool = False) -> None:
    """ 設定ファイルからユーザー情報を読み込み
    """
    config = load_config()
    if config is None:
        raise RuntimeError("Can not find ~/.brownianrc. Please setup ~/.brownianrc before use execute this command.")
    username = config.username
    password = config.password

    if username is None or password is None:
        raise RuntimeError("Can not read user id from dot file..")

    if sum([only_brand, only_stock, only_statments]) > 1:
        raise ValueError("Either of 'only_brand', 'only_stock', 'only_statements' can use.")

    do_stock = True
    do_brand = True
    do_statements = True
    do_yahoo = True

    if only_stock:
        do_stock = True
        do_brand = False
        do_statements = False
    if only_brand:
        do_stock = False
        do_brand = True
        do_statements = False
    if only_statments:
        do_stock = False
        do_brand = False
        do_statements = True
    if only_yahoo:
        do_stock = False
        do_brand = False
        do_statements = False
        do_yahoo = True

    repository_path = RepositoryPath(dir_path)

    if do_brand:
        # ブランド一覧を取得
        brand_crawler = BrandCrawler(repository_path, username, password)
        brand_crawler.crawl()

    if do_stock:
        # 株価情報を更新
        stock_crawler = DailyStockCrawler(repository_path, username, password)
        stock_crawler.crawl()

    if do_statements:
        # 決算情報の更新
        statements_crawler = DailyStatementsCrawler(repository_path, username, password)
        statements_crawler.crawl()

    if do_yahoo:
        # yahooから指数の情報を取得
        yahoo_crawler = YahooIndexCrawler(repository_path)
        yahoo_crawler.crawl()


class DailyStockCrawler:

    def __init__(self, repository_path: RepositoryPath, username: str, password: str,
                 logger: Optional[logging.Logger] = None) -> None:
        self.repository_path = repository_path
        self.username = username
        self.password = password

        self.crawl_start = datetime.date(2013, 4, 3)
        self.crawl_end = datetime.date.today()

        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def crawl(self, limit: Optional[int] = None, interval: Optional[int] = 1) -> None:
        # 初期化処理
        self.repository_path.setup_dir()
        login_token = self.login()
        if login_token is None:
            raise RuntimeError("Failed to login jquants")

        # limitが指定されている場合には取得日を制限
        date_ls = self.list_target_date()

        if limit is not None:
            size = min(len(date_ls), limit)
            date_ls = date_ls[:size]

        self.logger.info("Start crawling stock")

        success_count = 0
        fail_count = 0
        for d in date_ls:
            self.logger.info(f"Start downloading {d.strftime('%Y-%m-%d')}")
            try:
                # ダウンロードして保存
                df = jquants.donwload_daily_stock(login_token, d)
                filename = d.strftime("%Y-%m-%d.csv")
                filepath = self.repository_path.raw_stock_path / filename
                df.to_csv(filepath)
                success_count += 1
            except Exception as e:
                fail_count += 1
                self.logger.info(f"Fail downloading {d.strftime('%Y-%m-%d')}. Error: {e}")
            time.sleep(1)
            self.logger.info(f"Complete downloading {d.strftime('%Y-%m-%d')}")
        self.logger.info(f"Complete crawling. Successed {success_count}, Failed {fail_count}.")

    def login(self) -> Optional[str]:
        try:
            refresh_token = jquants.fetch_refresh_token(self.username, self.password)
            login_token = jquants.fetch_login_token(refresh_token)
            self.logger.info("Success to login.")
            return login_token
        except Exception:
            self.logger.info("Failed to login.")
            return None

    def list_target_date(self) -> List[datetime.date]:
        """ 取得対象の日付を列挙する
        """
        date_ls = workday_list(self.crawl_start, self.crawl_end)

        # 過去ダウンロードしていないデータのみダウンロードする
        already_download = []
        for dir in self.repository_path.raw_stock_path.iterdir():
            filename = dir.name.split(".")[0]
            try:
                date = datetime.datetime.strptime(filename, "%Y-%m-%d").date()
            except Exception:
                print(f"Can not parse {dir.name}")
            already_download.append(date)
        date_ls = list(filter(lambda x: x not in already_download, date_ls))
        return date_ls


class BrandCrawler:

    def __init__(self, repository_path: RepositoryPath, username: str, password: str, logger: Optional[logging.Logger] = None) -> None:
        self.repository_path = repository_path
        self.username = username
        self.password = password
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def crawl(self) -> None:
        # 初期化処理
        self.repository_path.setup_dir()
        login_token = self.login()
        if login_token is None:
            raise RuntimeError("Failed to login jquants")

        df = jquants.download_brand(login_token)
        filepath = self.repository_path.brand_path
        df.to_csv(filepath)
        self.logger.info("Success to download brand.csv.")

    def login(self) -> Optional[str]:
        try:
            refresh_token = jquants.fetch_refresh_token(self.username, self.password)
            login_token = jquants.fetch_login_token(refresh_token)
            self.logger.info("Success to login.")
            return login_token
        except Exception:
            self.logger.info("Failed to login.")
            return None


class DailyStatementsCrawler:

    def __init__(self, repository_path: RepositoryPath, username: str, password: str,
                 logger: Optional[logging.Logger] = None) -> None:
        self.repository_path = repository_path
        self.username = username
        self.password = password

        self.crawl_start = datetime.date(2013, 4, 3)
        self.crawl_end = datetime.date.today()

        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def crawl(self, limit: Optional[int] = None, interval: int = 1) -> None:
        # 初期化処理
        self.repository_path.setup_dir()
        login_token = self.login()
        if login_token is None:
            raise RuntimeError("Failed to login jquants")

        # limitが指定されている場合には取得日を制限
        date_ls = self.list_target_date()

        if limit is not None:
            size = min(len(date_ls), limit)
            date_ls = date_ls[:size]

        self.logger.info("Start crawling statements")
        success_count = 0
        fail_count = 0
        for d in date_ls:
            self.logger.info(f"Start downloading statements {d.strftime('%Y-%m-%d')}")
            try:
                # ダウンロードして保存
                df = jquants.donwload_daily_statements(login_token, d)
                filename = d.strftime("%Y-%m-%d.csv")
                filepath = self.repository_path.raw_statements_path / filename
                if df is not None:
                    df.to_csv(filepath)
                else:
                    filepath.touch()
                success_count += 1
            except Exception as e:
                fail_count += 1
                self.logger.info(f"Fail downloading statements {d.strftime('%Y-%m-%d')}. Error: {e}")
            time.sleep(interval)
            self.logger.info(f"Complete downloading statements {d.strftime('%Y-%m-%d')}")
        self.logger.info(f"Complete crawling. Successed {success_count}, Failed {fail_count}.")

    def login(self) -> Optional[str]:
        try:
            refresh_token = jquants.fetch_refresh_token(self.username, self.password)
            login_token = jquants.fetch_login_token(refresh_token)
            self.logger.info("Success to login.")
            return login_token
        except Exception:
            self.logger.info("Failed to login.")
            return None

    def list_target_date(self) -> List[datetime.date]:
        date_ls = workday_list(self.crawl_start, self.crawl_end)

        # 過去ダウンロードしていないデータのみダウンロードする
        already_download = []
        for dir in self.repository_path.raw_statements_path.iterdir():
            filename = dir.name.split(".")[0]
            try:
                date = datetime.datetime.strptime(filename, "%Y-%m-%d").date()
            except Exception as e:
                self.logger.warning(f"Can not parse {dir.name}")
                self.logger.exception(e)
            already_download.append(date)
        date_ls = list(filter(lambda x: x not in already_download, date_ls))
        return date_ls


class YahooIndexCrawler:

    def __init__(self, repository_path: RepositoryPath,
                 logger: Optional[logging.Logger] = None) -> None:
        self.repository_path = repository_path

    def crawl(self) -> None:

        target_pairs = [
            ("yahoo_gold", yahoo.COMODITY_GOLD),
            ("yahoo_oil", yahoo.COMODITY_CRUDE_OIL),
            ("yahoo_usd_jpy", yahoo.CURRENCY_USD_JPY),
            ("yahoo_eur_jpy", yahoo.CURRENCY_EUR_JPY),
            ("yahoo_dji", yahoo.INDEX_DJI),
            ("yahoo_sp500", yahoo.INDEX_SP500),
            ("yahoo_nikkei", yahoo.INDEX_NIKKEI),
            ("yahoo_dj_comodity", yahoo.INDEX_DJ_COMODITY),
            ("yahoo_msci_emerging", yahoo.INDEX_MSCI_EMERGING),
            ("yahoo_america_bond_5y", yahoo.BOND_AMERICA_5Y),
            ("yahoo_america_bond_10y", yahoo.BOND_AMERICA_10Y),
        ]

        start = datetime.date(2017, 1, 1)
        end = datetime.date.today()
        for name, key in target_pairs:
            try:
                logger.info(f"Downloading {key} since {start} to {end}")
                index = yahoo.download_index(key, start, end)
                repository = IndexCsvRepository(self.repository_path)
                repository.save(name, index)
            except Exception as e:
                logger.info(f"Error occrred while downloading {key}.")
                logger.exception(e)
            time.sleep(1)


def workday_list(first_date: datetime.date, last_date: datetime.date) -> List[datetime.date]:
    """ 営業日を列挙する
    """
    d = first_date
    cal = Calendar()
    ls = []
    while d <= last_date:
        if cal.is_business_day(d):
            ls.append(d)
        d += datetime.timedelta(days=1)
    return ls


if __name__ == "__main__":
    username = os.environ["J_QUANTS_USERNAME"]
    password = os.environ["J_QUANTS_PASSWORD"]
    refresh_token = jquants.fetch_refresh_token(username, password)
    login_token = jquants.fetch_login_token(refresh_token)
    df = jquants.download_market(login_token)
