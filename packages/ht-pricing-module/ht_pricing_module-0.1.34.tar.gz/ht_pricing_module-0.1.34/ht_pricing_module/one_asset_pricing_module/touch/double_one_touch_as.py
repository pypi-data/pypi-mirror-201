from ..one_asset_option_base import *


class DoubleOneTouch(OneAssetOptionBase):
    """
    双边界触碰期权 cash or nothing(连续)
    American Window
    reference: The Complete Guide to Option Pricing Formulas, 2nd ed. L177
    Double No touch option(DNT): 上涨或下跌失效 OUT,在同时不触碰上下障碍的情况下获得rebate
    Double One touch option(DOT): 上涨或下跌生效 IN, 在触碰上下障碍任意一个的情况下获得rebate
    One touch UP No touch Down(OTUNTD): 上涨生效下跌失效触碰期权, 在上障碍比下障碍先触碰的情况下获得rebate
    One touch DOWN No touch UP(OTDNTU): 下跌生效上涨失效触碰期权, 在下障碍比上障碍先触碰的情况下获得rebate

    OTDNTU + OTUNTD = DOT
    """

    def __G(self, T, mu, vol, xl, xh, ud, x) -> float:
        (k1, k2) = (np.arange(0, 7), np.arange(-6, 0))
        (u1, u2) = (ud * x + 2 * k1 * (xh - xl), ud * x + 2 * k2 * (xh - xl))
        (v, c) = (vol * np.sqrt(T), mu / vol ** 2)
        (e1, e2) = (np.exp(c * u1), np.exp(c * u2))
        pb1 = norm.cdf((-u1 - mu * T) / v) * e1 + norm.cdf((-u1 + mu * T) / v) / e1
        pb2 = norm.cdf((u2 + mu * T) / v) * e2 + norm.cdf((u2 - mu * T) / v) / e2
        return (np.sum(pb1) - np.sum(pb2)) * np.exp(c * x)

    def __VRbt(self, Rb, eh, T, mu_hat, mu_prime, vol, xl, xh, ud, x, DFr) -> float:
        if eh == RebateType.PAE:
            # PaE
            return Rb * DFr * self.__G(T, mu_hat, vol, xl, xh, ud, x)
        elif eh == RebateType.PAH:
            # PaH
            return Rb * np.exp((mu_hat - mu_prime) * x / vol ** 2) * self.__G(T, mu_prime, vol, xl, xh, ud, x)

    def __BS1D_dto_AW_CF(self, flag, S, T, r, q, vol, lb, ub, Rbt, pt) -> float:
        DFr = np.exp(-r * T)
        mu_hat = (r - q) - vol ** 2 / 2
        mu_prime = np.sqrt(mu_hat ** 2 + 2 * r * vol ** 2)
        (xl, xh) = (np.log(lb / S), np.log(ub / S))

        rst = 0
        if flag == 'OTUNTD':
            rst = self.__VRbt(Rbt, pt, T, mu_hat, mu_prime, vol, xl, xh, 1, xh, DFr)
        elif flag == 'OTDNTU':
            rst = self.__VRbt(Rbt, pt, T, mu_hat, mu_prime, vol, xl, xh, -1, xl, DFr)
        elif flag == 'DOT':
            OTDNTU = self.__BS1D_dto_AW_CF('OTDNTU', S, T, r, q, vol, lb, ub, Rbt, pt)
            OTUNTD = self.__BS1D_dto_AW_CF('OTUNTD', S, T, r, q, vol, lb, ub, Rbt, pt)
            rst = OTUNTD + OTDNTU
        elif flag == 'DNT':
            DOT = self.__BS1D_dto_AW_CF('DOT', S, T, r, q, vol, lb, ub, Rbt, pt)
            rst = Rbt * DFr - DOT

        return rst

    def __calculate_present_value__(self) -> float:
        rst = 0
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base

        u_knock_flag = self.param.spot_price >= self.param.upper_barrier_price
        d_knock_flag = self.param.spot_price <= self.param.lower_barrier_price

        if time_to_expiry <= 0:
            """已到期"""
            if self.param.knock_type == KnockType.IN:
                """触碰生效"""
                if self.param.is_knock_in or d_knock_flag or u_knock_flag:
                    """已敲入"""
                    return self.param.rebate
                else:
                    return 0
            elif self.param.knock_type == KnockType.OUT:
                """触碰失效"""
                if self.param.lower_barrier_price < self.param.spot_price < self.param.upper_barrier_price:
                    """触碰未失效"""
                    return self.param.rebate
                else:
                    return 0
        else:
            """存续"""
            if self.param.knock_type == KnockType.IN:
                if self.param.is_knock_in or d_knock_flag or u_knock_flag:
                    """生效"""
                    if self.param.rebate_type == RebateType.PAH:
                        return self.param.rebate
                    elif self.param.rebate_type == RebateType.PAE:
                        return self.param.rebate * np.exp(-self.param.riskfree_rate * time_to_expiry)
            elif self.param.knock_type == KnockType.OUT:
                if d_knock_flag or u_knock_flag:
                    """敲出失效"""
                    return 0

            if self.param.knock_type == KnockType.IN:
                # Double one touch
                rst = self.__BS1D_dto_AW_CF(flag='DOT',
                                            S=self.param.spot_price,
                                            T=time_to_expiry,
                                            r=self.param.riskfree_rate,
                                            q=self.param.dividend,
                                            vol=self.param.volatility,
                                            lb=self.param.lower_barrier_price,
                                            ub=self.param.upper_barrier_price,
                                            Rbt=self.param.rebate,
                                            pt=self.param.rebate_type)
            elif self.param.knock_type == KnockType.OUT:
                # Double no touch
                rst = self.__BS1D_dto_AW_CF(flag='DNT',
                                            S=self.param.spot_price,
                                            T=time_to_expiry,
                                            r=self.param.riskfree_rate,
                                            q=self.param.dividend,
                                            vol=self.param.volatility,
                                            lb=self.param.lower_barrier_price,
                                            ub=self.param.upper_barrier_price,
                                            Rbt=self.param.rebate,
                                            pt=RebateType.PAE)
            return rst
