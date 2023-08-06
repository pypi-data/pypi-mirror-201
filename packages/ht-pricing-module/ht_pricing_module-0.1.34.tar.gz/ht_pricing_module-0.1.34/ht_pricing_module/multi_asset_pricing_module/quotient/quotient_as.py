from ..multi_asset_option_base import *


class Quotient(MultiAssetOptionBase):

    def __calculate_present_value__(self):
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        s1_d_s2 = self.param.spot_price1 / self.param.spot_price2
        if time_to_expiry <= 0 or (self.param.volatility1 == 0 and self.param.volatility2 == 0):
            rst = max(cp * (s1_d_s2 - self.param.strike_price), 0)
        else:
            b1 = self.param.riskfree_rate - self.param.dividend1
            b2 = self.param.riskfree_rate - self.param.dividend2
            vol1_sq = math.pow(self.param.volatility1, 2)
            vol2_sq = math.pow(self.param.volatility2, 2)
            corr_vol1_sgi2 = self.param.correlation * self.param.volatility1 * self.param.volatility2
            sig_hat = np.sqrt(vol1_sq + vol2_sq - 2 * corr_vol1_sgi2)
            fut_hat = s1_d_s2 * np.exp((b1 - b2 + vol2_sq - corr_vol1_sgi2) * time_to_expiry)
            t_adj_vol = sig_hat * math.sqrt(time_to_expiry)
            discount_factor = math.exp(-1 * self.param.riskfree_rate * time_to_expiry)

            d1 = (math.log(fut_hat / self.param.strike_price) + (math.pow(sig_hat, 2) / 2.0) * time_to_expiry) / t_adj_vol
            d2 = d1 - t_adj_vol
            rst = discount_factor * cp * (fut_hat * norm.cdf(cp * d1) - self.param.strike_price * norm.cdf(cp * d2))
        return rst
