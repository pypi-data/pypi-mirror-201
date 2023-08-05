
import pathlib
from typing import List, Optional

import polars as pl
import tqdm

from ..models.statements import StatementsHistory
from .repository_path import RepositoryPath


class StatementsCSVRepository:

    def __init__(self, repository_path: RepositoryPath):
        self.repository_path = repository_path

    def load(self, limit=None, skip_error=True) -> List[StatementsHistory]:
        """ statementsディレクトリから決算情報を読み込む
        """
        statements_list = []
        dir_path = self.repository_path.statements_path
        filelist = list(dir_path.iterdir())

        if limit is not None:
            filelist = filelist[:limit]

        failed_ls = []
        for file in tqdm.tqdm(filelist):
            try:
                # CSVではなかった場合はスキップ
                if not file.name.endswith(".csv"):
                    continue
                # 空のファイルだった場合にはスキップする
                # この辺はis_readable_file()みたいな関数を用意したほうがいいかも
                statements = load_statements(file)
                if statements is None:
                    failed_ls.append(f"[*] {file} is empty file.")
                    continue

                statements_list.append(statements)
            except Exception as e:
                if not skip_error:
                    raise e
                failed_ls.append(f"[*] Failed to load {file}")
        for failed_log in failed_ls:
            self.log(failed_log)
        return statements_list

    def save(self, statements_list: List[StatementsHistory]) -> None:
        for s in tqdm.tqdm(statements_list):
            filename = self.repository_path.statements_path / f"{s.stock_code}.csv"
            s._df.write_csv(filename)

    def log(self, msg):
        print(msg)


def load_statements(csv_path: pathlib.Path) -> Optional[StatementsHistory]:
    if csv_path.stat().st_size == 0:
        return None
    df = pl.read_csv(csv_path)
    return StatementsHistory(df)
