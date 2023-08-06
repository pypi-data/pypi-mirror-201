from ..one_asset_option_base import *
from ..touch.one_touch_as import OneTouch


class DiscreteOneTouch(OneAssetOptionBase):
    """
    离散单触碰期权解析解
    """

    def __init__(self, param):
        super().__init__(param)
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        dt = self.param.obs_freq / self.param.year_base
        adjust = 0.5826 * self.param.volatility * math.sqrt(dt)
        if self.param.barrier_type == BarrierType.UP and time_to_expiry > 0:
            self.param.barrier_price = self.param.barrier_price * np.exp(adjust)
        elif self.param.barrier_type == BarrierType.DOWN and time_to_expiry > 0:
            self.param.barrier_price = self.param.barrier_price * np.exp(-adjust)

    def __calculate_present_value__(self) -> float:
        param = Struct({})
        param['spot_price'] = self.param.spot_price
        param['barrier_price'] = self.param.barrier_price
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['volatility'] = self.param.volatility
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['year_base'] = self.param.year_base
        param['barrier_type'] = self.param.barrier_type
        param['knock_type'] = self.param.knock_type
        param['is_knock_in'] = self.param.is_knock_in
        param['rebate_type'] = self.param.rebate_type
        param['rebate'] = self.param.rebate
        pricer = OneTouch(param)
        return pricer.present_value()
