from .protos import *

# 'CONTINUOUS', 'DISCRETE'
ObsType = protos_pricer.ObsType

# 'CALL', 'PUT', 'ACCUMULATOR', 'DECUMULATOR', 'STANDARD', 'REVERSE', 'ONE_TOUCH', 'DOUBLE_ONE_TOUCH
OptionType = protos_pricer.OptionType

# 'EUROPEAN', 'AMERICAN'
ExerciseType = protos_pricer.ExerciseType

# 'UP', 'DOWN'
BarrierType = protos_pricer.BarrierType

# 'IN', 'OUT'
KnockType = protos_pricer.KnockType

# 'PAH', 'PAE'
RebateType = protos_pricer.RebateType

# 'AS', 'MC', 'PDE'
PricingMethod = protos_pricer.PricingMethod

# 'LINEAR_ACC', 'FIXED_ACC', 'FIXED_ACC_AKO', 'FIXED_ACC_BARRIER', 'LINEAR_ACC_ENHANCED', 'FIXED_ACC_ENHANCED', 'LINEAR_ACC_AKO'
AccumulatorType = protos_pricer.AccumulatorType
