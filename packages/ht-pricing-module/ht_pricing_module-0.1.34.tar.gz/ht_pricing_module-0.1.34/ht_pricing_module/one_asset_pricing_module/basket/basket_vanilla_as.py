from ..one_asset_option_base import *


class BasketVanilla(OneAssetOptionBase):
    """
    篮子期权
    Bachelier model
    """
    def __calculate_present_value__(self) -> float:

        def __norm_pdf(x):
            return 1 / math.sqrt(2 * math.pi) * math.exp(-1 * pow(x, 2) / 2)

        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        if time_to_expiry <= 0:
            rst = max(cp * (self.param.spot_price - self.param.strike_price), 0)
        else:
            b = self.param.riskfree_rate - self.param.dividend
            f0 = self.param.spot_price * math.exp(b * time_to_expiry)
            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            discount_factor = math.exp(-1 * self.param.riskfree_rate * time_to_expiry)
            d = (f0 - self.param.strike_price) / t_adj_vol
            rst = discount_factor * (t_adj_vol * __norm_pdf(d) + cp * (f0 - self.param.strike_price) * norm.cdf(cp * d))
        return rst
