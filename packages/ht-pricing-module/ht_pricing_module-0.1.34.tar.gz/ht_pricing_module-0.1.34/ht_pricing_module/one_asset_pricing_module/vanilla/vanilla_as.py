from ..one_asset_option_base import *


class Vanilla(OneAssetOptionBase):

    def __calculate_present_value__(self):
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        if time_to_expiry <= 0 or self.param.volatility == 0:
            rst = max(cp * (self.param.spot_price - self.param.strike_price), 0)
        else:
            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            d1 = (math.log(self.param.spot_price / self.param.strike_price) + (self.param.riskfree_rate - self.param.dividend + math.pow(self.param.volatility, 2) / 2.0) * time_to_expiry) / t_adj_vol
            d2 = d1 - t_adj_vol
            rst = cp * self.param.spot_price * math.exp(-1 * self.param.dividend * time_to_expiry) * norm.cdf(cp * d1) -\
                  cp * self.param.strike_price * math.exp(-1 * self.param.riskfree_rate * time_to_expiry) * norm.cdf(cp * d2)
        return rst
