from ..one_asset_option_base import *


class OneTouch(OneAssetOptionBase):
    """
    触碰期权 cash or nothing(连续)
    American Window
    reference: The Complete Guide to Option Pricing Formulas, 2nd ed. L177
    No touch option(NT): 上涨或下跌失效 OUT,触碰障碍期权失效无赔付,不触碰障碍到期赔付rebate
    One touch option(OT): 上涨或下跌生效 IN, 触碰障碍立即支付或到期支付rebate,不触碰障碍到期无赔付

    OTD + NTD = rebate * exp(-r * t)
    OTU + NTU = rebate * exp(-r * t)
    """

    def __calculate_present_value__(self) -> float:
        rst = 0
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base

        u_knock_flag = self.param.barrier_type == BarrierType.UP and self.param.spot_price >= self.param.barrier_price
        d_knock_flag = self.param.barrier_type == BarrierType.DOWN and self.param.spot_price <= self.param.barrier_price

        if time_to_expiry <= 0:
            """已到期"""
            if self.param.knock_type == KnockType.IN:
                """触碰生效"""
                if self.param.is_knock_in or u_knock_flag or d_knock_flag:
                    """敲入"""
                    return self.param.rebate
                else:
                    return 0
            elif self.param.knock_type == KnockType.OUT:
                """触碰失效"""
                if u_knock_flag or d_knock_flag:
                    """失效"""
                    return 0
                else:
                    return self.param.rebate
        else:
            """存续"""
            if self.param.knock_type == KnockType.IN:
                if self.param.is_knock_in or u_knock_flag or d_knock_flag:
                    """生效"""
                    if self.param.rebate_type == RebateType.PAH:
                        return self.param.rebate
                    elif self.param.rebate_type == RebateType.PAE:
                        return self.param.rebate * np.exp(-self.param.riskfree_rate * time_to_expiry)
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出失效"""
                    return 0

            """触碰期权(连续)解析解"""
            du = {BarrierType.DOWN: 1, BarrierType.UP: -1}[self.param.barrier_type]
            eh = {KnockType.IN: -du, KnockType.OUT: du}[self.param.knock_type]

            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            exp_r_t = np.exp(-1 * self.param.riskfree_rate * time_to_expiry)
            vol_sq = math.pow(self.param.volatility, 2)
            ba_d_sp = self.param.barrier_price / self.param.spot_price

            mu = (self.param.riskfree_rate - self.param.dividend - vol_sq / 2) / vol_sq
            lamda = math.sqrt(math.pow(mu, 2) + 2 * self.param.riskfree_rate / vol_sq)

            x2 = np.log(self.param.spot_price / self.param.barrier_price) / t_adj_vol + (1 + mu) * t_adj_vol
            y2 = np.log(ba_d_sp) / t_adj_vol + (1 + mu) * t_adj_vol
            z = np.log(ba_d_sp) / t_adj_vol + lamda * t_adj_vol

            B2 = self.param.rebate * exp_r_t * norm.cdf(eh * x2 - eh * t_adj_vol)
            B4 = self.param.rebate * exp_r_t * math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y2 - du * t_adj_vol)
            A5 = self.param.rebate * (math.pow(ba_d_sp, mu + lamda) * norm.cdf(du * z) +
                                      math.pow(ba_d_sp, mu - lamda) * norm.cdf(du * z - 2 * du * lamda * t_adj_vol))

            if self.param.knock_type == KnockType.IN:
                # one touch
                rst = {RebateType.PAE: B2 + B4, RebateType.PAH: A5}[self.param.rebate_type]
            elif self.param.knock_type == KnockType.OUT:
                # no touch
                rst = B2 - B4
            return rst
