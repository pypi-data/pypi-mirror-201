from ..one_asset_option_base import *


class Asian(OneAssetOptionBase):
    """
    算术平均亚式期权(连续)
    reference: The Complete Guide to Option Pricing Formulas, 2nd ed. L186
    :param running_avg: 已实现平均价格
    :param obs_start_date: 价格平均观测期开始日期
    """

    def __calculate_present_value__(self) -> float:
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        time_to_obs = (self.param.current_date - self.param.obs_start_date) / self.param.year_base
        add_time = time_to_expiry + time_to_obs

        b = self.param.riskfree_rate - self.param.dividend
        vol_sq = math.pow(self.param.volatility, 2)
        spot_sq = math.pow(self.param.spot_price, 2)
        discount_factor = math.exp(-1 * self.param.riskfree_rate * time_to_expiry)

        if time_to_expiry <= 0:
            """已到期"""
            rst = max(cp * (self.param.running_avg - self.param.strike_price), 0)
        else:
            """存续"""
            if time_to_obs < 0:
                """未进入价格平均观测期"""
                if self.param.riskfree_rate == self.param.dividend:
                    p1 = 1
                    p2 = 2 * (math.exp(add_time * vol_sq) - 1 - add_time * vol_sq) / math.pow(vol_sq * add_time, 2)
                else:
                    p1 = (math.exp(b * add_time) - 1) / b / add_time
                    p21 = 2 * math.exp((2 * b + vol_sq) * add_time)
                    p22 = (b + vol_sq) * (2 * b + vol_sq) * math.pow(add_time, 2)
                    p23 = 2 / b / math.pow(add_time, 2)
                    p24 = 1 / (2 * b + vol_sq)
                    p25 = math.exp(b * add_time) / (b + vol_sq)
                    p2 = p21 / p22 + p23 * (p24 - p25)
                var = math.log(p2 / p1 / p1) + vol_sq * (-1 * time_to_obs)
                f0 = p1 * self.param.spot_price * math.exp(b * (-1 * time_to_obs))
                b1 = (math.log(f0 / self.param.strike_price) + 0.5 * var) / math.sqrt(var)
                b2 = (math.log(f0 / self.param.strike_price) - 0.5 * var) / math.sqrt(var)
                rst = discount_factor * (cp * f0 * norm.cdf(cp * b1) - cp * self.param.strike_price * norm.cdf(cp * b2))
            else:
                """进入价格平均观测期"""
                if self.param.riskfree_rate == self.param.dividend:
                    m1 = self.param.spot_price
                    m2 = 2 * spot_sq * (math.exp(time_to_expiry * vol_sq) - 1 - time_to_expiry * vol_sq) / math.pow((vol_sq * time_to_expiry), 2)
                else:
                    m1 = (math.exp(b * time_to_expiry) - 1) * self.param.spot_price / b / time_to_expiry
                    m21 = 2 * math.exp((2 * b + vol_sq) * time_to_expiry) * spot_sq
                    m22 = (b + vol_sq) * (2 * b + vol_sq) * math.pow(time_to_expiry, 2)
                    m23 = 2 * spot_sq / b / math.pow(time_to_expiry, 2)
                    m24 = 1 / (2 * b + vol_sq)
                    m25 = math.exp(b * time_to_expiry) / (b + vol_sq)
                    m2 = m21 / m22 + m23 * (m24 - m25)
                f0 = m1
                var = 1 / time_to_expiry * math.log(m2 / m1 / m1)
                k = add_time / time_to_expiry * self.param.strike_price - time_to_obs / time_to_expiry * self.param.running_avg
                if k > 0:
                    b1 = (math.log(f0 / k) + 0.5 * var * time_to_expiry) / math.sqrt(var * time_to_expiry)
                    b2 = b1 - math.sqrt(var * time_to_expiry)
                    rst = discount_factor * (cp * f0 * norm.cdf(cp * b1) - cp * k * norm.cdf(cp * b2)) * time_to_expiry / add_time
                else:
                    if cp == 1:
                        rst = time_to_expiry / add_time * (m1 - k) * discount_factor
                    else:
                        rst = 0
        return rst
