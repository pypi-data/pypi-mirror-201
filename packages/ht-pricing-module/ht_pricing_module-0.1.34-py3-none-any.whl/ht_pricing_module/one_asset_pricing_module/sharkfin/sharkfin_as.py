from ..one_asset_option_base import *
from ..binary.binary_as import Binary
from ..vanilla.vanilla_as import Vanilla


class Sharkfin(OneAssetOptionBase):
        
    def __calculate_present_value__(self):
        if self.param.strike_price == self.param.barrier_price:
            return 0

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
        vanilla1 = Vanilla(param)

        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        gt = 1 if (self.param.strike_price - self.param.barrier_price) > 0 else -1
        if cp * gt > 0:
            return vanilla1.present_value()

        param = Struct({})
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price
        param['strike_price'] = self.param.barrier_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['year_base'] = self.param.year_base
        vanilla2 = Vanilla(param)

        param = Struct({})
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price
        param['strike_price'] = self.param.barrier_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['payoff'] = abs(self.param.strike_price - self.param.barrier_price)
        param['year_base'] = self.param.year_base
        binary1 = Binary(param)

        return vanilla1.present_value() - vanilla2.present_value() - binary1.present_value()
