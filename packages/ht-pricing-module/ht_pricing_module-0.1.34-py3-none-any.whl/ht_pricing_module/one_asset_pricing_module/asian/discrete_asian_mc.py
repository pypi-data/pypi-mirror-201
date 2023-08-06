from ..one_asset_option_base import *


class DiscreteAsianMc(OneAssetOptionBase):
    """
    算术平均离散亚视期权MC
    :param obs_date: 离散观测日，包括：历史观测日及已实现价格和未来观测日
    """

    def __calculate_present_value__(self) -> float:
        residual_intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
        current_date_index = math.floor(self.param.current_date)
        return self.mc_asian(
            option_type=self.param.option_type,
            spot_price=self.param.spot_price,
            strike_price=self.param.strike_price,
            running_avg=self.param.running_avg,
            riskfree_rate=self.param.riskfree_rate,
            dividend=self.param.dividend,
            volatility=self.param.volatility,
            residual_intraday=residual_intraday,
            expiry_date=self.param.expiry_date - current_date_index,
            year_base=self.param.year_base,
            obs=[[obs.obs_index - current_date_index, obs.obs_price]for obs in self.param.obs_date]
        )

    def mc_asian(self, option_type, spot_price, strike_price, running_avg, riskfree_rate, dividend, volatility,
                 residual_intraday, expiry_date, year_base, obs):

        cp = 1 if option_type == OptionType.CALL else - 1
        rst = 0
        if expiry_date <= 0:
            rst = max(cp * (np.mean(running_avg) - strike_price), 0)
        else:
            intraday = round(math.ceil(residual_intraday) - residual_intraday, 4)
            gmb = McPathGenerator.generate(riskfree_rate=riskfree_rate, dividend=dividend, volatility=volatility,
                                           intraday=intraday, expiry_date=expiry_date, year_base=year_base, random_seed=0)
            price = spot_price * gmb
            obs = np.array(obs)
            obs_index_arr = obs[obs[:, 0] >= 0][:, 0].astype(int)
            obs_price_arr = obs[obs[:, 0] < 0][:, 1]

            discount_factor = np.exp(-1 * riskfree_rate * (expiry_date - intraday) / year_base)
            avg_price_arr = np.mean(np.concatenate((np.tile(obs_price_arr, (len(price), 1)), price[:, obs_index_arr]), axis=1), axis=1)
            rst = np.mean(discount_factor * np.maximum(cp * (avg_price_arr - strike_price), 0))
        return rst
