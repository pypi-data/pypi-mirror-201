

class Brand():

    """ 銘柄情報を扱うクラス
    """

    def __init__(self, code, company_name, sector17, sector33, scale_category, market_code):
        self.code = code
        self.company_name = company_name
        self.sector17 = sector17
        self.sector33 = sector33
        self.scale_category = scale_category
        self.market_code = market_code

    def __repr__(self):
        return self.company_name

    def __eq__(self, other):
        if not isinstance(other, Brand):
            raise TypeError("other must be Brand object.")
        return other.code == self.code
