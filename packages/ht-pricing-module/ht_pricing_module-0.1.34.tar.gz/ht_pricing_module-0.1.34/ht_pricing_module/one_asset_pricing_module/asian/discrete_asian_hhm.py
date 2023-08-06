from ..one_asset_option_base import *


class DiscreteAsianHhm(OneAssetOptionBase):
    """
    算术平均离散亚式期权近似解析解(daily)
    reference: The Complete Guide to Option Pricing Formulas, 2nd ed. L194
    :param running_avg: 已实现平均价格
    :param obs_start_date: 价格平均观测期开始日期
    """

    def __calculate_present_value__(self) -> float:
        n = (self.param.expiry_date - self.param.obs_start_date) + 1
        m = max(0.0, (self.param.current_date - self.param.obs_start_date) + 1)
        T = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        t1 = max(1.0, (self.param.obs_start_date - self.param.current_date)) / self.param.year_base

        b = self.param.riskfree_rate - self.param.dividend
        X = self.param.strike_price
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]

        if T <= 0:
            """已到期"""
            return max(cp * (self.param.running_avg - X), 0)

        """存续"""
        if m == n - 1:
            X_hat = n * X - (n - 1) * self.param.running_avg
            d1 = (np.log(self.param.spot_price / X_hat) + (0.5 * math.pow(self.param.volatility, 2)) * T) / (self.param.volatility * np.sqrt(T))
            d2 = d1 - self.param.volatility * np.sqrt(T)
            rst = np.exp(-self.param.riskfree_rate * T) * (cp * self.param.spot_price * norm.cdf(cp * d1) - cp * X_hat * norm.cdf(cp * d2)) / n
            if ~np.isnan(rst):
                return rst

        h = (T - t1) / (n - 1)
        if b == 0:
            EA = self.param.spot_price
            EA2 = math.pow(self.param.spot_price, 2) * np.exp(math.pow(self.param.volatility, 2) * t1) / (n * n) * \
                  ((1 - np.exp(math.pow(self.param.volatility, 2) * h * n)) / (1 - np.exp(math.pow(self.param.volatility, 2) * h)) +
                   2 / (1 - np.exp(math.pow(self.param.volatility, 2) * h)) * (n - (1 - np.exp(math.pow(self.param.volatility, 2) * h * n)) / (1 - np.exp(math.pow(self.param.volatility, 2) * h))))
        else:
            EA = self.param.spot_price / n * np.exp(b * t1) * (1 - np.exp(b * h * n)) / (1 - np.exp(b * h))
            EA2 = math.pow(self.param.spot_price, 2) * np.exp((2 * b + math.pow(self.param.volatility, 2)) * t1) / (n * n) \
                  * ((1 - np.exp((2 * b + math.pow(self.param.volatility, 2)) * h * n)) / (1 - np.exp((2 * b + math.pow(self.param.volatility, 2)) * h))
                     + 2 / (1 - np.exp((b + math.pow(self.param.volatility, 2)) * h)) * ((1 - np.exp(b * h * n)) / (1 - np.exp(b * h))
                                                         - (1 - np.exp((2 * b + math.pow(self.param.volatility, 2)) * h * n))
                                                         / (1 - np.exp((2 * b + math.pow(self.param.volatility, 2)) * h))))

        if m > 0:
            if self.param.running_avg > n / m * X:
                if self.param.option_type == OptionType.PUT:
                    return 0
                else:
                    RA_hat = self.param.running_avg * m / n + EA * (n - m) / n
                    return np.exp(-self.param.riskfree_rate * T) * (RA_hat - X)

        vA = np.sqrt((np.log(EA2) - 2 * np.log(EA)) / T)

        if m > 0:
            X = n / (n - m) * X - m / (n - m) * self.param.running_avg

        d1 = (np.log(EA / X) + vA * vA / 2 * T) / (vA * np.sqrt(T))
        d2 = d1 - vA * np.sqrt(T)
        rst = np.exp(-self.param.riskfree_rate * T) * (cp * EA * norm.cdf(cp * d1) - cp * X * norm.cdf(cp * d2))
        return rst * (n - m) / n