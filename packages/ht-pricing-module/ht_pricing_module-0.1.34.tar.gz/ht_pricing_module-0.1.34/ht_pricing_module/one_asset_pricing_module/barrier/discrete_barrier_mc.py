from ..one_asset_option_base import *
from ..vanilla.vanilla_as import Vanilla


class DiscreteBarrierMc(OneAssetOptionBase):
    """
    离散障碍期权MC
    :param obs_date: 离散观测日
    """

    def __calculate_present_value__(self) -> float:
        if self.param.is_knock_in and self.param.knock_type == KnockType.IN:
            # vanilla
            param = Struct({})
            param['option_type'] = self.param.option_type
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['expiry_date'] = self.param.expiry_date
            param['current_date'] = self.param.current_date
            param['volatility'] = self.param.volatility
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['year_base'] = self.param.year_base
            vanilla = Vanilla(param)
            return vanilla.present_value()
        else:
            # mc
            residual_intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
            current_date_index = math.floor(self.param.current_date)
            return self.mc_barrier(
                option_type=self.param.option_type,
                knock_type=self.param.knock_type,
                barrier_type=self.param.barrier_type,
                spot_price=self.param.spot_price,
                strike_price=self.param.strike_price,
                barrier_price=self.param.barrier_price,
                rebate=self.param.rebate,
                riskfree_rate=self.param.riskfree_rate,
                dividend=self.param.dividend,
                volatility=self.param.volatility,
                residual_intraday=residual_intraday,
                expiry_date=self.param.expiry_date - current_date_index,
                year_base=self.param.year_base,
                obs=[obs.obs_index - current_date_index for obs in self.param.obs_date]
            )

    def mc_barrier(self, option_type, knock_type, barrier_type, spot_price, strike_price, barrier_price, rebate,
                   riskfree_rate, dividend, volatility, residual_intraday, expiry_date, year_base, obs):

        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[option_type]
        io = {KnockType.IN: 1, KnockType.OUT: -1}[knock_type]
        ud = {BarrierType.UP: 1, BarrierType.DOWN: -1}[barrier_type]
        rst = 0

        if expiry_date <= 0:
            knock = 1 if ud * (spot_price - barrier_price) >= 0 else -1
            if knock * io == 1:
                rst = max(cp * (spot_price - strike_price), 0)
            elif knock * io == -1:
                rst = (0 if io == 1 else 1) * rebate
        else:
            intraday = round(math.ceil(residual_intraday) - residual_intraday, 4)
            gbm = McPathGenerator.generate(riskfree_rate=riskfree_rate, dividend=dividend, volatility=volatility,
                                           intraday=intraday, expiry_date=expiry_date, year_base=year_base, random_seed=0)

            price = spot_price * gbm

            obs_arr = np.array(obs).astype(int)
            obs_arr = obs_arr[obs_arr >= 0]

            knock_flag = ud * (price[:, obs_arr] - barrier_price) >= 0
            knock_index = (np.insert(knock_flag, 0, np.zeros(len(knock_flag)), axis=1)).argmax(axis=1)

            if io == 1:
                knock_index = np.where(knock_index > 0, 1, 0)
                discount_factor = np.exp(-1 * riskfree_rate * (expiry_date - intraday) / year_base)
                value = np.multiply(knock_index.T, np.maximum(cp * (price[:, -1] - strike_price), 0))
                value = value + np.multiply((1 - knock_index).T, rebate)
                rst = np.mean(discount_factor * value)
            else:
                discount_factor_arr = np.exp(-1 * riskfree_rate * (obs_arr - intraday) / year_base)
                discount_factor_arr = np.insert(discount_factor_arr, 0, 0)[knock_index]
                discount_factor = np.exp(-1 * riskfree_rate * (expiry_date - intraday) / year_base)
                knock_index = np.where(knock_index > 0, 1, 0)
                value = np.multiply(discount_factor_arr.T, rebate * knock_index)
                value = value + discount_factor * np.multiply((1 - knock_index).T, np.maximum(cp * (price[:, -1] - strike_price), 0))
                rst = np.mean(value)
        return rst
