from ..one_asset_option_base import *
from ..binary.binary_as import Binary


class BarrierBinary(OneAssetOptionBase):
    """
    二元障碍 cash or nothing 解析解
    reference: The Complete Guide to Option Pricing Formulas, 2nd ed. L152
    """

    def __calculate_present_value__(self) -> float:
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        du = {BarrierType.DOWN: 1, BarrierType.UP: -1}[self.param.barrier_type]
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base

        u_knock_flag = self.param.barrier_type == BarrierType.UP and self.param.spot_price >= self.param.barrier_price
        d_knock_flag = self.param.barrier_type == BarrierType.DOWN and self.param.spot_price <= self.param.barrier_price

        if time_to_expiry <= 0:
            """已到期"""
            if self.param.knock_type == KnockType.IN:
                if self.param.is_knock_in or u_knock_flag or d_knock_flag:
                    """敲入"""
                    return self.param.payoff if cp * (self.param.spot_price - self.param.strike_price) >= 0 else 0
                else:
                    return 0
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出"""
                    return 0
                else:
                    return self.param.payoff if cp * (self.param.spot_price - self.param.strike_price) >= 0 else 0
        else:
            """存续"""
            if self.param.knock_type == KnockType.IN:
                if self.param.is_knock_in or u_knock_flag or d_knock_flag:
                    """敲入"""

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
                    param['payoff'] = self.param.payoff
                    param['year_base'] = self.param.year_base
                    pricer = Binary(param)
                    return pricer.present_value()
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出"""
                    return 0

            """障碍二元期权(连续)解析解"""
            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            exp_r_t = np.exp(-1 * self.param.riskfree_rate * time_to_expiry)
            vol_sq = math.pow(self.param.volatility, 2)
            ba_d_sp = self.param.barrier_price / self.param.spot_price

            mu = (self.param.riskfree_rate - self.param.dividend - vol_sq / 2) / vol_sq
            lamda = math.sqrt(math.pow(mu, 2) + 2 * self.param.riskfree_rate / vol_sq)

            x1 = np.log(self.param.spot_price / self.param.strike_price) / t_adj_vol + (1 + mu) * t_adj_vol
            x2 = np.log(self.param.spot_price / self.param.barrier_price) / t_adj_vol + (1 + mu) * t_adj_vol
            y1 = np.log(math.pow(self.param.barrier_price, 2) / (self.param.spot_price * self.param.strike_price)) / t_adj_vol + (1 + mu) * t_adj_vol
            y2 = np.log(ba_d_sp) / t_adj_vol + (1 + mu) * t_adj_vol
            z = np.log(ba_d_sp) / t_adj_vol + lamda * t_adj_vol

            B1 = self.param.payoff * exp_r_t * norm.cdf(cp * x1 - cp * t_adj_vol)
            B2 = self.param.payoff * exp_r_t * norm.cdf(cp * x2 - cp * t_adj_vol)

            B3 = self.param.payoff * exp_r_t * math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y1 - du * t_adj_vol)
            B4 = self.param.payoff * exp_r_t * math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y2 - du * t_adj_vol)

            cp = {OptionType.CALL: 'c', OptionType.PUT: 'p'}[self.param.option_type]
            du = {BarrierType.DOWN: 'd', BarrierType.UP: 'u'}[self.param.barrier_type]
            io = {KnockType.IN: 'i', KnockType.OUT: 'o'}[self.param.knock_type]

            rst = {'cdi': B3 if self.param.strike_price >= self.param.barrier_price else B1 - B2 + B4,
                   'cui': B1 if self.param.strike_price >= self.param.barrier_price else B2 - B3 + B4,
                   'pdi': B2 - B3 + B4 if self.param.strike_price >= self.param.barrier_price else B1,
                   'pui': B1 - B2 + B4 if self.param.strike_price >= self.param.barrier_price else B3,
                   'cdo': B1 - B3 if self.param.strike_price >= self.param.strike_price else B2 - B4,
                   'cuo': 0 if self.param.strike_price >= self.param.barrier_price else B1 - B2 + B3 - B4,
                   'pdo': B1 - B2 + B3 - B4 if self.param.strike_price >= self.param.barrier_price else 0,
                   'puo': B2 - B4 if self.param.strike_price >= self.param.barrier_price else B1 - B3}[f'{cp}{du}{io}']
        return rst

