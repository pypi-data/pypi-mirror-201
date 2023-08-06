
from collections import defaultdict
from typing import DefaultDict, Dict, ItemsView


class Order:

    """ 注文を表現するクラス
    """

    def __init__(self) -> None:
        self.num_dict: DefaultDict[str, int] = defaultdict(int)

    def buy(self, code: str, num: int) -> None:
        """ 買い銘柄を登録する
        """
        self.num_dict[code] += num

    def sell(self, code: str, num: int) -> None:
        """ 売り銘柄を登録する
        """
        self.num_dict[code] -= num

    def buy_iter(self) -> ItemsView[str, int]:
        """ 買い銘柄に限定したイテレータを返す
        """
        ret: Dict[str, int] = {}
        for key, value in self.num_dict.items():
            if value > 0:
                ret[key] = value
        return ret.items()

    def sell_iter(self) -> ItemsView[str, int]:
        ret: Dict[str, int] = {}
        for key, value in self.num_dict.items():
            if value < 0:
                ret[key] = abs(value)
        return ret.items()

    def show(self) -> None:
        print("[*] Buy list")
        for code, num in self.buy_iter():
            print(f"{code}: {num}")

        print("[*] Sell list")
        for code, num in self.sell_iter():
            print(f"{code}: {num}")
