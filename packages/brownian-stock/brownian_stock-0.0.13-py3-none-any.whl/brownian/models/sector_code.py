

class SectorCode:

    """ Topixの17分類を表すクラス
    """

    def __init__(self, name, code):
        self.__name = name
        self.__code = code

    @property
    def name(self):
        return self.__name

    @property
    def code(self):
        return self.__code

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, int):
            return self.code == __o
        if isinstance(__o, SectorCode):
            return self.code == __o.code
        raise ValueError("Only int or sector code can compare.")

    def __hash__(self):
        return self.code

    def __repr__(self):
        return f"{self.__code}-{self.__name}"

    def __str__(self) -> str:
        return f"{self.__code}-{self.__name}"


sector_dict = {
    1: SectorCode("食品", 1),
    2: SectorCode("エネルギー資源", 2),
    3: SectorCode("建設・資材", 3),
    4: SectorCode("医薬品", 4),
    5: SectorCode("素材・科学", 5),
    6: SectorCode("自動車・輸送機", 6),
    7: SectorCode("鉄鋼・非鉄", 7),
    8: SectorCode("機械", 8),
    9: SectorCode("電気・精密", 9),
    10: SectorCode("情報通信・サービスその他", 10),
    11: SectorCode("電気・ガス", 11),
    12: SectorCode("運輸・物流", 12),
    13: SectorCode("商社・卸売", 13),
    14: SectorCode("小売", 14),
    15: SectorCode("銀行", 15),
    16: SectorCode("金融（除く銀行）", 16),
    17: SectorCode("不動産", 17)
}
else_code = SectorCode("その他", 99)


def build_sector_code(code):
    return sector_dict.get(code, else_code)


class SectorConst:
    FOOD = build_sector_code(1)
    ENERGY_RESOURCES = build_sector_code(2)
    CONSTRUCTION_MATERIALS = build_sector_code(3)
    MATERIAL_CHEMICAL = build_sector_code(4)
    PHARMACEUTICALS = build_sector_code(5)
    TRANSPORTATION_MACHINE = build_sector_code(6)
    STEEL_NONFERROUS = build_sector_code(7)
    MACHINE = build_sector_code(8)
    ELECTRONICS_PRECISION = build_sector_code(9)
    INFORMATION_SERVICE = build_sector_code(10)
    ELECTRICAL_GAS = build_sector_code(11)
    TRANSPORTATION_LOGISTICS = build_sector_code(12)
    TRADING_COMPANY_WHOLESALE = build_sector_code(13)
    RETAIL = build_sector_code(14)
    BANK = build_sector_code(15)
    FINANCE_EXCLUDE_BANKS = build_sector_code(16)
    REAL_ESTATE = build_sector_code(17)
    ELSE = build_sector_code(99)

    @classmethod
    def sector_list(cls):
        return [
            cls.FOOD,
            cls.ENERGY_RESOURCES,
            cls.CONSTRUCTION_MATERIALS,
            cls.MATERIAL_CHEMICAL,
            cls.PHARMACEUTICALS,
            cls.TRANSPORTATION_MACHINE,
            cls.STEEL_NONFERROUS,
            cls.MACHINE,
            cls.ELECTRONICS_PRECISION,
            cls.INFORMATION_SERVICE,
            cls.ELECTRICAL_GAS,
            cls.TRANSPORTATION_LOGISTICS,
            cls.TRADING_COMPANY_WHOLESALE,
            cls.RETAIL,
            cls.BANK,
            cls.FINANCE_EXCLUDE_BANKS,
            cls.REAL_ESTATE,
            cls.ELSE
        ]
