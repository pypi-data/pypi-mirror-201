from ..one_asset_option_base import *


class Forward(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        return self.param.spot_price - self.param.strike_price
