

""" 実際の売買のシミュレーションを提供する
"""

import cProfile
import datetime
import logging
import pathlib
import pstats
import time
from typing import List, Optional

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

from .models.abstract_model import AbstractModel

logger = logging.getLogger(__name__)


class AccountHistory:

    def __init__(self, name: str) -> None:
        self.name = name
        self.date_list :List[datetime.date] = []
        self.valuation_list :List[float] = []

    def push(self, trade_date: datetime.date, valuation: float) -> None:
        self.date_list.append(trade_date)
        self.valuation_list.append(valuation)

    def show(self) -> None:
        first_valuation = self.valuation_list[0]
        last_valuation = self.valuation_list[-1]

        valuation_array: np.ndarray = np.array(self.valuation_list)
        pct_change = np.diff(valuation_array) / valuation_array[:-1]

        avg_return = np.mean(pct_change) * 100
        std_return = np.std(pct_change) * 100
        sharp_ratio = avg_return / std_return

        print(f"[*] Trading Result of {self.name}")
        print(f"Valuation: {last_valuation / first_valuation}")
        print(f"Average Daily Return: {avg_return:.3f}% ± {std_return:.3f} bp")
        print(f"Sharp Ratio: {sharp_ratio :.3f}")
        print("")


class Simulator():

    """
    Args:
        trading_model(AbstractModel): 評価対象の取引モデル
        save_figure(optional: None or str): 評価額の推移の画像を保存するディレクトリ名

    Usage:
    >> simu = Simulator(model)
    >> valuation = simu.walk(datetime.date(2022, 12, 1), datetime.date(2022, 12, 31))
    >> print(valuation)
    1000000
    """
    def __init__(self, trading_model: AbstractModel, account_list: List[AbstractModel], save_figure: Optional[str] = None) -> None:
        self.trading_model = trading_model
        self.initial_buying_power :Optional[int] = None
        self.figure_dir = save_figure

        self.account_list = account_list
        self.history_list = [AccountHistory(a.name()) for a in account_list]

        # Figure Name
        self.figure_path = None
        if self.figure_dir is not None:
            now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"valuation_history_{now_str}.png"
            self.figure_path = pathlib.Path(self.figure_dir, filename)

    def init_state(self, buying_power: int) -> None:
        self.initial_buying_power = buying_power

        self.trading_model.init_state(buying_power)
        for account_i in self.account_list:
            account_i.init_state(buying_power)

    def walk(self, start_date: datetime.date, end_date: datetime.date, display_progress: bool = True,
             enable_profile :bool = False) -> int:
        """ 実際のシミュレーション処理
        """
        if self.initial_buying_power is None:
            raise RuntimeError("Call init_state before walk.")
        for history_i in self.history_list:
            history_i.push(start_date, self.initial_buying_power)

        start_time = time.time()
        today = start_date
        count = 0
        while today <= end_date:
            # 10回に一回グラフを描画
            count += 1
            if count % 10 == 0 and self.figure_dir is not None:
                self.show_graph()

            # 取引を実行
            if enable_profile:
                prof = cProfile.Profile()
                prof.enable()
 
            return_map = self.trading_model.trade(today)
            if return_map is not None:
                for account_i, history_i in zip(self.account_list, self.history_list):
                    account_i.execute(today, return_map)
                    valuation = account_i.valuation(today)
                    if display_progress:
                        print(f"{today} {account_i.name()}: {valuation}")
                    history_i.push(today, valuation)
            else:
                logger.info("Order is None. Skip trading.")

            if enable_profile:
                prof.disable()
                sort_key = pstats.SortKey.CUMULATIVE  # NOQA
                stats = pstats.Stats(prof).sort_stats(sort_key)
                stats.print_stats(20)

            # 日の終了処理
            self.trading_model.day_close(today)
            today += datetime.timedelta(days=1)

        for history_i in self.history_list:
            history_i.show()

        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time:.3f}")
        # 画像を保存する必要があれば保存する
        if self.figure_dir:
            self.show_graph()
        return valuation

    def show_graph(self) -> None:
        # 描画領域の調整
        if self.figure_path is None:
            return
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(1, 1, 1)
        fig.subplots_adjust(bottom=0.2)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
        ax.tick_params(axis='x', labelrotation=45)

        # グラフを描画
        for history_i in self.history_list:
            label = history_i.name
            x = history_i.date_list
            y = history_i.valuation_list
            ax.plot(x, y, label=label)
        ax.legend()

        # ファイルを保存
        fig.savefig(self.figure_path)
