from ..one_asset_option_base import *
from ..vanilla.vanilla_as import Vanilla


class RatioSpread(OneAssetOptionBase):

    def __calculate_present_value__(self):
        param = Struct({})
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price
        param['strike_price'] = self.param.spot_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['year_base'] = self.param.year_base
        vanilla1 = Vanilla(param)

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
        vanilla2 = Vanilla(param)

        return vanilla1.present_value() - self.param.leverage * vanilla2.present_value()
