from ..monte_carlo_engine import *
from ..api_and_utils import *


class OneAssetOptionBase:

    def __init__(self, param):
        self.param = Struct(param) if isinstance(param, dict) else param

    def __calculate_present_value__(self) -> float:
        raise NotImplementedError()

    # @lru_cache
    def present_value(self) -> float:
        return self.__calculate_present_value__()

    # @lru_cache
    def delta(self, step: float = 0.001) -> float:
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        if time_to_expiry <= 0:
            return 0.0

        if hasattr(self.param, 'spot_price'):
            spot_up = self.param.spot_price * (1 + step)
            spot_down = self.param.spot_price * (1 - step)
            pricer_up = deepcopy(self)
            pricer_up.param.spot_price = spot_up
            pricer_down = deepcopy(self)
            pricer_down.param.spot_price = spot_down
            return (pricer_up.present_value() - pricer_down.present_value()) / (spot_up - spot_down)
        return 0.0

    # @lru_cache
    def gamma(self, step: float = 0.001) -> float:
        if hasattr(self.param, 'spot_price'):
            spot_up = self.param.spot_price * (1 + step)
            spot_down = self.param.spot_price * (1 - step)
            pricer_up = deepcopy(self)
            pricer_up.param.spot_price = spot_up
            pricer_down = deepcopy(self)
            pricer_down.param.spot_price = spot_down
            return (pricer_up.present_value() + pricer_down.present_value() - 2 * self.present_value()) / pow((spot_up - spot_down) / 2, 2) 
        return 0.0

    # @lru_cache
    def vega(self, step: float = 0.01) -> float:
        if hasattr(self.param, 'volatility'):
            vol_up = self.param.volatility + step
            pricer_up = deepcopy(self)
            pricer_up.param.volatility = vol_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    # @lru_cache
    def theta(self, step: float = 1) -> float:
        if hasattr(self.param, 'current_date'):
            current_up = self.param.current_date + step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    # @lru_cache
    def rho(self, step: float = 0.0001) -> float:
        if hasattr(self.param, 'riskfree_rate'):
            current_up = self.param.riskfree_rate + step
            pricer_up = deepcopy(self)
            pricer_up.param.riskfree_rate = current_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    # @lru_cache
    def ddeltadt(self, time_step: float = 1, price_step: float = 0.001):
        if hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price'):
            current_up = self.param.current_date + time_step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            return pricer_up.delta(step=price_step) - self.delta(step=price_step)
        return 0.0

    # @lru_cache
    def ddeltadv(self, vol_step: float = 0.01, price_step: float = 0.001):
        if hasattr(self.param, 'volatility') and hasattr(self.param, 'spot_price'):
            vol_up = self.param.volatility + vol_step
            pricer_up = deepcopy(self)
            pricer_up.param.volatility = vol_up
            return pricer_up.delta(step=price_step) - self.delta(step=price_step)
        return 0.0
