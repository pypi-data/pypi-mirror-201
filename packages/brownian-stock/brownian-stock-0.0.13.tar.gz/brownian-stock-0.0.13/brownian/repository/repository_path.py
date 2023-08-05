
import os
import pathlib
from typing import Union

DIR_RAW_STOCK = "raw_stock"
DIR_RAW_INDEX = "raw_index"
DIR_TMP = "tmp"
DIR_TMP_STATEMENTS = "tmp_statements"

CSV_BRAND = "brand.csv"
CSV_TMP_BRAND = "tmp_brand.csv"
CSV_TOPIX = "topix.csv"
CSV_TMP_TOPIX = "tmp_topix.csv"


class RepositoryPath:

    """ レポジトリフォルダのパスを表現するクラス

        self.dir_path = pathlib.Path(dir_path)
        # 生の株価情報
        self.raw_stock_path = self.dir_path / DIR_RAW_STOCK
        # 財務情報
        self.raw_statements_path = self.dir_path / DIR_RAW_STATEMENTS
        self.tmp_statements_path = self.dir_path / DIR_TMP_STATEMENTS
        # 一時フォルダ
        self.tmp_path = self.dir_path / DIR_TMP
        # 銘柄情報のCSV
        self.brand_csv_path = self.dir_path / CSV_BRAND
        self.brand_tmp_path = self.dir_path / CSV_TMP_BRAND
        # TOPIXの情報
        self.raw_index_path = self.dir_path / DIR_RAW_INDEX
        self.topix_csv_path = self.raw_index_path / CSV_TOPIX
        self.topix_tmp_path = self.raw_index_path / CSV_TMP_TOPIX
    """
    def __init__(self, dir_path: Union[str, pathlib.Path]) -> None:
        if isinstance(dir_path, pathlib.Path):
            self.dir_path = dir_path
        elif isinstance(dir_path, str):
            self.dir_path = pathlib.Path(dir_path)
        else:
            raise TypeError("dir_path must be str or pathlib.Path object.")

    def setup_dir(self) -> None:
        check_ls = [
            self.root_path,
            self.stock_path,
            self.statements_path,
            self.raw_stock_path,
            self.raw_statements_path
        ]
        for path in check_ls:
            if not path.exists():
                os.makedirs(path)

    @property
    def root_path(self) -> pathlib.Path:
        """ Repositoryのルートパス
        """
        return self.dir_path

    @property
    def sqlite_path(self) -> pathlib.Path:
        return self.dir_path / "sqlite3.db"

    @property
    def brand_path(self) -> pathlib.Path:
        return self.dir_path / "brand.csv"

    @property
    def raw_stock_path(self) -> pathlib.Path:
        """ JQuantsからダウンロードした生CSVの保存場所
        """
        return self.dir_path / "raw_stock"

    @property
    def stock_path(self) -> pathlib.Path:
        """ 整形した各銘柄の株価情報
        """
        return self.dir_path / "stock"

    @property
    def comodity_path(self) -> pathlib.Path:
        return self.dir_path / "comodity"

    @property
    def raw_statements_path(self) -> pathlib.Path:
        """ ダウンロードした財務情報の保存場所
        """
        return self.dir_path / "raw_statements"

    @property
    def statements_path(self) -> pathlib.Path:
        """ 整形した決算情報の保存場所
        """
        return self.dir_path / "statements"

    @property
    def tmp_statements_path(self) -> pathlib.Path:
        """ 財務情報の保存場所　
        """
        return self.dir_path / DIR_TMP_STATEMENTS
