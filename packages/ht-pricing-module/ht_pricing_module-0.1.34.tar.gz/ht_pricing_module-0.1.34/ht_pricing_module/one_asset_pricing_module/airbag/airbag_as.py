from ..one_asset_option_base import *
from ..barrier import DiscreteBarrier
from ..forward import Forward


class Airbag(OneAssetOptionBase):

    def __calculate_present_value__(self):
        phi = {OptionType.STANDARD: 1, OptionType.REVERSE: -1}[self.param.option_type]

        if self.param.strike_price == self.param.barrier_price or self.param.is_knock_in or\
                (self.param.option_type == OptionType.STANDARD and self.param.spot_price <= self.param.barrier_price) or\
                (self.param.option_type == OptionType.REVERSE and self.param.spot_price >= self.param.barrier_price):
            param = Struct({})
            param['spot_price'] = self.param.spot_price
            param['strike_price'] = self.param.strike_price
            forward = Forward(param=param)
            return phi * forward.present_value()

        barrier_type = {OptionType.STANDARD: BarrierType.DOWN,
                        OptionType.REVERSE: BarrierType.UP}[self.param.option_type]
        knock_out_option_type = {OptionType.STANDARD: OptionType.CALL,
                                 OptionType.REVERSE: OptionType.PUT}[self.param.option_type]

        param = Struct({})
        param['option_type'] = OptionType.CALL
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
        param['knock_type'] = KnockType.IN
        param['is_knock_in'] = self.param.is_knock_in
        param['rebate'] = 0
        param['obs_freq'] = self.param.obs_freq
        barrier1 = DiscreteBarrier(param)

        param = Struct({})
        param['option_type'] = OptionType.PUT
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
        param['knock_type'] = KnockType.IN
        param['is_knock_in'] = self.param.is_knock_in
        param['rebate'] = 0
        param['obs_freq'] = self.param.obs_freq
        barrier2 = DiscreteBarrier(param)

        param = Struct({})
        param['option_type'] = knock_out_option_type
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
        param['is_knock_in'] = self.param.is_knock_in
        param['rebate'] = 0
        param['obs_freq'] = self.param.obs_freq
        barrier3 = DiscreteBarrier(param)

        return phi * (barrier1.present_value() - barrier2.present_value()) + self.param.participation_rate * barrier3.present_value()
