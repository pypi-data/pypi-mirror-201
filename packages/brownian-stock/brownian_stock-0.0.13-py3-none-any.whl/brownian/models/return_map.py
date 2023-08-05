
from __future__ import annotations

from typing import Dict, List, Set, Union


class ReturnMap:

    """ 各銘柄のスコアを表すクラス
    """

    def __init__(self) -> None:
        self.return_map :Dict[str, float] = {}

    def on_same_universe(self, other: ReturnMap) -> bool:
        if not isinstance(other, ReturnMap):
            raise TypeError("other must be ReturnMap object.")
        set1 = set(self.return_map.keys())
        set2 = set(other.return_map.keys())
        return set1 == set2

    def __len__(self) -> int:
        return len(self.return_map)

    def __contains__(self, key: str) -> bool:
        return key in self.return_map.keys()

    def __add__(self, other: Union[ReturnMap, int, float]) -> ReturnMap:
        """ 数値または同じUniverseを持つotherに対して足し算を定義する.
        """
        if isinstance(other, ReturnMap):
            if not self.on_same_universe(other):
                diff = self.diff(other)
                raise ValueError(f"`other` must have same universe of self. Diff: {diff}")
            new_map = ReturnMap()
            for key in self.return_map.keys():
                v1 = self.return_map.get(key, None)
                v2 = other.return_map.get(key, None)
                if v1 is None or v2 is None:
                    raise ValueError("ReturnMap contains None")
                new_map[key] = self.return_map[key] + other.return_map[key]
            return new_map
        if isinstance(other, int) or isinstance(other, float):
            new_map = ReturnMap()
            for key, value in self.return_map.items():
                if value is None:
                    raise ValueError("ReturnMap contains None")
                new_map[key] = value + other
            return new_map
        raise ValueError("other must be a instance of ReturmMap or number")

    def __mul__(self, other: Union[int, float]) -> ReturnMap:
        """ 数値に対して掛け算を定義する.
        """
        if not isinstance(other, int) and not isinstance(other, float):
            raise ValueError("other must be a number")

        new_map = ReturnMap()
        for key, value in self.return_map.items():
            if value is not None:
                new_map[key] = value * other
            else:
                new_map[key] = value
        return new_map

    def __getitem__(self, key: str) -> float:
        return self.return_map[key]

    def __setitem__(self, key: str, value: float) -> None:
        self.return_map[key] = value

    def __delitem__(self, key: str) -> None:
        del self.return_map[key]

    def diff(self, other: ReturnMap) -> Set[str]:
        """ selfとotherの銘柄の差分を取る
        Args:
            other(ReturmMap)
        Return:
            list of str
        """
        # ２つのsetの排他的論理和を取る
        set1 = set(self.return_map.keys())
        set2 = set(other.return_map.keys())
        return set1 ^ set2

    def intersection(self, other: ReturnMap) -> ReturnMap:
        # ２つのsetの積を取る
        set1 = set(self.return_map.keys())
        set2 = set(other.return_map.keys())
        intersection = set1 & set2

        new_map = ReturnMap()
        for key in intersection:
            new_map[key] = self[key]
        return new_map

    def standardize(self) -> ReturnMap:
        """ 最大値と最小値で標準化した新しいReturnMapを返す
        """
        values = self.return_map.values()
        min_v = float(min(values))
        max_v = float(max(values))

        new_map = ReturnMap()
        for key, value in self.return_map.items():
            new_map[key] = (value - min_v) / (max_v - min_v)
        return new_map

    def ranked(self) -> ReturnMap:
        keys = self.return_map.keys()
        values = self.return_map.values()
        s = sorted(values)

        ranked = [s.index(x) for x in values]
        minv = min(ranked)
        maxv = max(ranked)
        ranked = [(r - minv) / (maxv - minv) for r in ranked]
        new_map = ReturnMap()
        for key, value in zip(keys, ranked):
            new_map[key] = value
        return new_map

    def ordered_code_list(self, asc :bool = False) -> List[str]:
        """ 銘柄をスコア順に並び替えて返します.
        デフォルトで降順で数字を返します.
        """
        tuple_list = [(score, code) for code, score in self.return_map.items()]
        tuple_list = sorted(tuple_list, key=lambda x: x[0], reverse=not asc)
        code_list = [code for _, code in tuple_list]
        return code_list

    def show(self, limit=100) -> None:
        code_list = self.ordered_code_list()
        size = min(len(code_list), limit)
        for code in code_list[:size]:
            score = self.return_map[code]
            print(f"{code}: {score:.3f}")

    def remove_none(self) -> ReturnMap:
        new_map = ReturnMap()
        for key, value in self.return_map.items():
            if value is not None:
                new_map[key] = value
        return new_map