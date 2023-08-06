from ..one_asset_option_base import *


class DiscreteBinaryMc(OneAssetOptionBase):
    """
    离散观测二元MC
    :param obs_date: 离散观测日
    """

    def __calculate_present_value__(self) -> float:
        residual_intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
        current_date_index = math.floor(self.param.current_date)
        return self.mc_binary(
            option_type=self.param.option_type,
            spot_price=self.param.spot_price,
            strike_price=self.param.strike_price,
            payoff=self.param.payoff,
            riskfree_rate=self.param.riskfree_rate,
            dividend=self.param.dividend,
            volatility=self.param.volatility,
            residual_intraday=residual_intraday,
            expiry_date=self.param.expiry_date - current_date_index,
            year_base=self.param.year_base,
            obs=[obs.obs_index - current_date_index for obs in self.param.obs_date]
        )

    def mc_binary(self, option_type, spot_price, strike_price, payoff, riskfree_rate, dividend, volatility,
                  residual_intraday, expiry_date, year_base, obs):

        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[option_type]
        rst = 0

        if expiry_date <= 0:
            rst = payoff if cp * (spot_price - strike_price) >= 0 else 0
        else:
            intraday = round(math.ceil(residual_intraday) - residual_intraday, 4)
            gbm = McPathGenerator.generate(riskfree_rate=riskfree_rate, dividend=dividend, volatility=volatility,
                                           intraday=intraday, expiry_date=expiry_date, year_base=year_base,
                                           random_seed=0)

            price = spot_price * gbm

            obs_arr = np.array(obs).astype(int)
            obs_arr = obs_arr[obs_arr >= 0]

            payoff_flag = cp * (price[:, obs_arr] - strike_price) >= 0
            payoff_index = (np.insert(payoff_flag, 0, np.zeros(len(payoff_flag)), axis=1)).argmax(axis=1)
            discount_factor_arr = np.exp(-1 * riskfree_rate * (obs_arr - intraday) / year_base)
            discount_factor_arr = np.insert(discount_factor_arr, 0, 0)[payoff_index]
            rst = np.mean(payoff * discount_factor_arr)
        return rst
