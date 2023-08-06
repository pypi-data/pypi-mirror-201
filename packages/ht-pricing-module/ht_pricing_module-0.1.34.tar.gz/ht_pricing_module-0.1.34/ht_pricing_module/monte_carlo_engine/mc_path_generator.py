from ..api_and_utils import np, qmc, warnings, lru_cache, wraps

warnings.filterwarnings('ignore')


def mc_np_cache(function):
    @lru_cache
    def cached_wrapper(qmc_flag, antithetic_flag, random_seed, M, drift, volatility, hashable_array):
        return function(qmc_flag, antithetic_flag, random_seed, M, drift, volatility,  np.array(hashable_array))

    @wraps(function)
    def wrapper(qmc_flag, antithetic_flag, random_seed, M, drift, volatility, array):
        return cached_wrapper(qmc_flag, antithetic_flag, random_seed, M, drift, volatility, tuple(array))

    wrapper.cache_info = cached_wrapper.cache_info
    wrapper.cache_clear = cached_wrapper.cache_clear
    return wrapper


@mc_np_cache
def generate_randn(qmc_flag, antithetic_flag, random_seed, M, drift, volatility, dt_arr):
    """生成标准正态分布随机数矩阵"""
    N = len(dt_arr)
    if qmc_flag:
        randn = qmc.MultivariateNormalQMC(mean=np.zeros(N), cov=np.eye(N), seed=random_seed).random(M)
    else:
        np.random.seed(random_seed)
        randn = np.random.randn(M, N)
    if antithetic_flag:
        randn = np.vstack([randn, -randn])

    log_rtn = drift * dt_arr + volatility * np.sqrt(dt_arr) * randn
    cum_log_rtn = np.cumsum(log_rtn, axis=1)
    cum_log_rtn = np.hstack([np.zeros([len(cum_log_rtn), 1]), cum_log_rtn])
    exp_cum_log_rtn = np.exp(cum_log_rtn)
    return exp_cum_log_rtn


class McPathGenerator:
    """

    蒙特卡洛路径生成函数，输出结果为spot价格为1的几何布朗运动
    :param riskfree_rate: 无风险利率
    :param dividend: 分红率
    :param volatility: 波动率
    :param intraday: 日内时间
    :param expiry_date: 到日期离当前日收盘天数
    :param year_base: 年化日历天数
    :param path_num: 路径数
    :param antithetic_flag: 是否使用对偶变量
    :param qmc_flag: 是否使用quasi-monte carlo，使用Sobol低差异化序列
    :param random_seed: 指定随机种子

    e.g.
    intraday = 0.2
    expiry_date = 252
    剩余整数天数为252天，当前日内时间为0.8天，当日剩余天数为0.2天，则剩余到期时间为251.2天。
    生成时间序列为[0, 0.2, 1.2, 2.2, ... 251.2], 长度为253；
    生成时间间隔dt序列为[0.2, 1, 1, 1, ... 1], 长度为252；
    返回长度为253的几何布朗运动，其中第一列是1，为当前时刻价格，后面252列为每个观测日(日终)；
    将返回矩阵乘以当前价格即可得到价格路径。
    """

    @classmethod
    def generate(cls, riskfree_rate, dividend, volatility, intraday, expiry_date, year_base,
                 path_num=100000, antithetic_flag=True, qmc_flag=True, random_seed=None):
        drift = riskfree_rate - dividend - 0.5 * volatility ** 2
        t_arr = np.arange(1, expiry_date + 1, 1) - intraday
        t_arr = np.hstack([0, t_arr])
        dt_arr = (t_arr[1:] - t_arr[:-1]) / year_base
        gmb_trn = generate_randn(qmc_flag, antithetic_flag, random_seed, path_num, drift, volatility, dt_arr)
        return gmb_trn
