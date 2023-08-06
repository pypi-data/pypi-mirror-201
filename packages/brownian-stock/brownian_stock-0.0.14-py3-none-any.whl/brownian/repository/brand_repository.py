
from typing import List

import polars as pl

from ..models.brand import Brand
from .repository_path import RepositoryPath


class BrandRepository:

    def __init__(self, repository_path: RepositoryPath):
        self.repository_path = repository_path

    def load(self) -> List[Brand]:
        brand_ls = []
        conn = self.__get_connection()
        brand_df = pl.read_sql("SELECT * FROM brand;", conn).to_pandas()
        for _, row in brand_df.iterrows():
            code = row["Code"]
            company_name = row["CompanyName"]
            sector17 = row["Sector17Code"]
            sector33 = row["Sector33Code"]
            scale_category = row["ScaleCategory"]
            market_code = row["MarketCode"]
            brand = Brand(code, company_name, sector17, sector33, scale_category, market_code)
            brand_ls.append(brand)
        return brand_ls

    def __get_connection(self) -> str:
        """ Sqlite用のConnectionStringを生成する
        https://sfu-db.github.io/connector-x/databases/sqlite.html
        """
        conn = "sqlite://" + str(self.repository_path.sqlite_path.absolute())
        return conn
