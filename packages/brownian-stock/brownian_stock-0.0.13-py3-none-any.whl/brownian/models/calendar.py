
# from typing import Self
from __future__ import annotations

import calendar
import datetime
import json
import logging
import pathlib

import requests

CALENDAR_PATH = pathlib.Path(__file__).parents[1] / "data" / "calendar.json"
logger = logging.getLogger(__name__)


class Calendar:

    """ 東証の営業日を管理するクラス
    CSVを読み込むため生成コストがやや高いのでget_instanceで
    singleton化されたインスタンスを取得するのが好ましい.
    """

    instance = None

    @classmethod
    def get_instance(cls) -> Calendar:
        if cls.instance is None:
            cls.instance = Calendar()
        return cls.instance

    def __init__(self) -> None:
        with open(CALENDAR_PATH, "r") as fp:
            calendar_list = json.load(fp)
        calendar_list = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in calendar_list]
        self.calendar_set = set(calendar_list)

    def is_business_day(self, d: datetime.date) -> bool:
        """ 指定した日が営業日かどうか判定する. 営業日ならばTrue
        """
        if d.weekday() in [5, 6]:
            return False
        if d in self.calendar_set:
            return False
        return True

    def last_business_day(self, d: datetime.date) -> datetime.date:
        # 安全のため最大でも365日しか遡らない
        for i in range(1, 365):
            target_date = d - datetime.timedelta(days=i)
            if self.is_business_day(target_date):
                return target_date
        raise RuntimeError("Reach Error, program cant't reach this line.")

    def days_from_last_business_day(self, d: datetime.date) -> int:
        """ 前営業日から何日経過したか判定する
        """

        # 安全のため最大でも365日しか遡らない
        elapsed = 0
        for i in range(1, 365):
            target_date = d - datetime.timedelta(days=i)
            if self.is_business_day(target_date):
                return elapsed
            elapsed += 1
        raise RuntimeError("Reach Error, program cant't reach this line.")

    def record_date_of_month(self, d: datetime.date) -> datetime.date:
        """ 指定した日と同月の権利付き最終日(=月末から3営業日前)
        日本においては監修として決算日 = 権利付き最終日という文化があるので
        当該ロジックで問題ないとは思う.
        """
        year = d.year
        month = d.month
        date = calendar.monthrange(year, month)[1]
        month_last = datetime.date(year, month, date)

        # 月末から3営業日前を返す
        count = 0
        for i in range(31):
            target_date = month_last - datetime.timedelta(days=i)
            if self.is_business_day(target_date):
                count += 1

            if count == 3:
                return target_date
        raise RuntimeError("Reach Error, program cant't reach this line.")


def create_calendar_csv() -> None:
    """ 2010年から2030年までのカレンダーを作成し, brownian/data/以下に保存する
    生成にあたって以下のルールに準拠する.
    * 国民の祝日は休業日
    * 12/31, 1/1, 1/2, 1/3は休日
    """
    url = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding
    holiday_set = []
    holiday_lines = resp.text.split("\n")

    for line in holiday_lines:
        line = line.strip()
        if line == "":
            continue
        try:
            # 一応parseできるか確認するためにdate化する
            date_str = line.split(",")[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
            holiday_set.append(date_obj.strftime("%Y-%m-%d"))
        except Exception as e:
            print(f"Raise Error while parsing text `{line}`, {e}")

    # 年末年始を登録する
    first_year = 2010
    last_year = 2030

    for year in range(first_year, last_year + 1):
        holiday_set.append(f"{year}-1-1")
        holiday_set.append(f"{year}-1-2")
        holiday_set.append(f"{year}-1-3")
        holiday_set.append(f"{year}-12-31")
    holiday_set = sorted(holiday_set)
    holiday_set = list(set(holiday_set))

    with open(CALENDAR_PATH, "w") as fp:
        json.dump(holiday_set, fp)


if __name__ == "__main__":
    create_calendar_csv()
