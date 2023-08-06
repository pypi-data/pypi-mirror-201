from ..one_asset_option_base import *
from ..vanilla.vanilla_as import Vanilla


class Barrier(OneAssetOptionBase):
    """
    障碍期权(连续)
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
                    return max(cp * (self.param.spot_price - self.param.strike_price), 0)
                else:
                    return self.param.rebate
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出"""
                    return self.param.rebate
                else:
                    return max(cp * (self.param.spot_price - self.param.strike_price), 0)
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
                    param['year_base'] = self.param.year_base
                    pricer = Vanilla(param)
                    return pricer.present_value()
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出"""
                    return self.param.rebate

            """障碍期权(连续)解析解"""
            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            exp_q_t = np.exp(-1 * self.param.dividend * time_to_expiry)
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

            A = cp * self.param.spot_price * exp_q_t * norm.cdf(cp * x1) - \
                cp * self.param.strike_price * exp_r_t * norm.cdf(cp * x1 - cp * t_adj_vol)
            B = cp * self.param.spot_price * exp_q_t * norm.cdf(cp * x2) - \
                cp * self.param.strike_price * exp_r_t * norm.cdf(cp * x2 - cp * t_adj_vol)

            C = cp * self.param.spot_price * exp_q_t * math.pow(ba_d_sp, 2 * (mu + 1)) * norm.cdf(du * y1) - \
                cp * self.param.strike_price * exp_r_t * math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y1 - du * t_adj_vol)
            D = cp * self.param.spot_price * exp_q_t * math.pow(ba_d_sp, 2 * (mu + 1)) * norm.cdf(du * y2) - \
                cp * self.param.strike_price * exp_r_t * math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y2 - du * t_adj_vol)

            E = self.param.rebate * exp_r_t * (norm.cdf(du * x2 - du * t_adj_vol) -
                                               math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y2 - du * t_adj_vol))
            F = self.param.rebate * (math.pow(ba_d_sp, mu + lamda) * norm.cdf(du * z) +
                                     math.pow(ba_d_sp, mu - lamda) * norm.cdf(du * z - 2 * du * lamda * t_adj_vol))

            cp = {OptionType.CALL: 'c', OptionType.PUT: 'p'}[self.param.option_type]
            du = {BarrierType.DOWN: 'd', BarrierType.UP: 'u'}[self.param.barrier_type]
            io = {KnockType.IN: 'i', KnockType.OUT: 'o'}[self.param.knock_type]

            rst = {'cdi': C + E if self.param.strike_price >= self.param.barrier_price else A - B + D + E,
                   'cui': A + E if self.param.strike_price >= self.param.barrier_price else B - C + D + E,
                   'pdi': B - C + D + E if self.param.strike_price >= self.param.barrier_price else A + E,
                   'pui': A - B + D + E if self.param.strike_price >= self.param.barrier_price else C + E,
                   'cdo': A - C + F if self.param.strike_price >= self.param.barrier_price else B - D + F,
                   'cuo': F if self.param.strike_price >= self.param.barrier_price else A - B + C - D + F,
                   'pdo': A - B + C - D + F if self.param.strike_price >= self.param.barrier_price else F,
                   'puo': B - D + F if self.param.strike_price >= self.param.barrier_price else A - C + F}[f'{cp}{du}{io}']
        return rst
