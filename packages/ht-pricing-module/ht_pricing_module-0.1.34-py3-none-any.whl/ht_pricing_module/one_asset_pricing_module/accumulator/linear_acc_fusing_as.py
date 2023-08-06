from ..one_asset_option_base import *
from ..barrier.discrete_barrier_as import DiscreteBarrier


class LinearAccFusing(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        rst = 0

        leveraged_barrier_option_type = {OptionType.ACCUMULATOR: OptionType.PUT,
                                         OptionType.DECUMULATOR: OptionType.CALL}[self.param.option_type]
        non_leveraged_barrier_option_type = {OptionType.ACCUMULATOR: OptionType.CALL,
                                             OptionType.DECUMULATOR: OptionType.PUT}[self.param.option_type]
        barrier_type = {OptionType.ACCUMULATOR: BarrierType.UP,
                        OptionType.DECUMULATOR: BarrierType.DOWN}[self.param.option_type]

        for obs in self.param.obs_date:
            param = Struct({})
            param['option_type'] = leveraged_barrier_option_type
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = obs.obs_price if self.param.current_date > obs.obs_index else self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['barrier_price'] = self.param.barrier_price
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['volatility'] = self.param.volatility
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['year_base'] = self.param.year_base
            param['barrier_type'] = barrier_type
            param['knock_type'] = KnockType.OUT
            param['is_knock_in'] = 0
            param['rebate'] = 0
            param['obs_freq'] = self.param.obs_freq
            leveraged_barrier = DiscreteBarrier(param)

            param = Struct({})
            param['option_type'] = non_leveraged_barrier_option_type
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = obs.obs_price if self.param.current_date > obs.obs_index else self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['barrier_price'] = self.param.barrier_price
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['volatility'] = self.param.volatility
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['year_base'] = self.param.year_base
            param['barrier_type'] = barrier_type
            param['knock_type'] = KnockType.OUT
            param['is_knock_in'] = 0
            param['rebate'] = self.param.payoff
            param['obs_freq'] = self.param.obs_freq
            non_leveraged_barrier = DiscreteBarrier(param)

            rst = rst + (-self.param.leverage * leveraged_barrier.present_value() + non_leveraged_barrier.present_value())

        param = Struct({})
        param['option_type'] = leveraged_barrier_option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price
        param['strike_price'] = self.param.strike_price
        param['barrier_price'] = self.param.barrier_price
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['volatility'] = self.param.volatility
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['year_base'] = self.param.year_base
        param['barrier_type'] = barrier_type
        param['knock_type'] = KnockType.OUT
        param['is_knock_in'] = 0
        param['rebate'] = 0
        param['obs_freq'] = self.param.obs_freq
        fusing_barrier = DiscreteBarrier(param)

        rst = rst - fusing_barrier.present_value() * self.param.final_position_multiplier
        return rst

    # @lru_cache
    def theta(self, step: float = 1) -> float:
        if hasattr(self.param, 'current_date'):
            current_up = self.param.current_date + step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            for obs in pricer_up.param.obs_date:
                if self.param.current_date <= obs.obs_index < pricer_up.param.current_date:
                    obs.obs_price = pricer_up.param.spot_price
            return pricer_up.present_value() - self.present_value()
        return 0.0

    # @lru_cache
    def ddeltadt(self, time_step: float = 1, price_step: float = 0.001):
        if hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price'):
            current_up = self.param.current_date + time_step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            for obs in pricer_up.param.obs_date:
                if self.param.current_date <= obs.obs_index < pricer_up.param.current_date:
                    obs.obs_price = pricer_up.param.spot_price
            return pricer_up.delta(step=price_step) - self.delta(step=price_step)
        return 0.0
