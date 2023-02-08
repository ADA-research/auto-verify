from enum import Enum

from ConfigSpace import Categorical, ConfigurationSpace, Float, Integer


class BranchMode(Enum):
    BRANCH_OVERAPPROX = 0
    BRANCH_EGO = 1
    BRANCH_EGO_LIGHT = 2
    BRANCH_EXACT = 3


class SplitOrder(Enum):
    SPLIT_LARGEST = 0
    SPLIT_ONE_NORM = 1
    SPLIT_SMALLEST = 2
    SPLIT_INORDER = 3


class OverApproxTypes(Enum):
    za = ["zono.area"]
    za_zy_zi = ["zono.area", "zono.ybloat", "zono.interval"]
    za_zy_zi_sl = ["zono.area", "zono.ybloat", "zono.interval", "star.lp"]


nnenum_configspace = ConfigurationSpace(name="nnenum")


compress_init_box = Categorical("COMPRESS_INIT_BOX ", [True, False])
eager_bounds = Categorical("EAGER_BOUNDS", [True, False])
contract_zonotope = Categorical("CONTRACT_ZONOTOPE", [True, False])
contract_zonotope_lp = Categorical("CONTRACT_ZONOTOPE_LP", [True, False])
contract_lp_optimized = Categorical("CONTRACT_LP_OPTIMIZED", [True, False])
contract_lp_track_witnesses = Categorical("CONTRACT_LP_TRACK_WITNESSES", [True, False])
contract_lp_check_epsilon = Categorical("CONTRACT_LP_CHECK_EPSILON", [True, False])
overapprox_types = Categorical("OVERAPPROX_TYPES", [e.name for e in OverApproxTypes])
overapprox_near_root_max_splits = Integer(
    "OVERAPPROX_NEAR_ROOT_MAX_SPLITS", default=2, bounds=[1, 3]
)
# TODO: Depends on OVERAPPROX_TYPES, add condition
overapprox_types_near_root = Categorical("OVERAPPROX_TYPES_NEAR_ROOT", [True, False])
overapprox_gen_limit_multiplier = Float(
    "OVERAPPROX_GEN_LIMIT_MULTIPLIER", default=1.5, bounds=[1, 2]
)
overapprox_min_gen_limit = Integer(
    "OVERAPPROX_MIN_GEN_LIMIT", default=50, bounds=[25, 75]
)
overapprox_lp_timeout = Float("OVERAPPROX_LP_TIMEOUT", default=1.0, bounds=[0.5, 1.5])
overapprox_both_bounds = Categorical("OVERAPPROX_BOTH_BOUNDS", [True, False])
branch_mode = Categorical("BRANCH_MODE", [e.value for e in BranchMode])
try_quick_overapprox = Categorical("TRY_QUICK_OVERAPPROX", [True, False])
quick_overapprox_types = Categorical(
    "QUICK_OVERAPPROX_TYPES",
    [
        OverApproxTypes(["zono.area"]),
        OverApproxTypes(["zono.area", "zono.ybloat", "zono.interval"]),
    ],
)
split_order = Categorical("SPLIT_ORDER", [e.value for e in SplitOrder])
result_save_polys_epsilon = Float(
    "RESULT_SAVE_POLYS_EPSILON", default=1e-7, bounds=[1e-6, 1e-8]
)
split_tolerance = Float("SPLIT_TOLERANCE", default=1e-8, bounds=[1e-7, 1e-9])
split_if_idle = Categorical("SPLIT_IF_IDLE", [True, False])
shuffle_time = Categorical("SHUFFLE_TIME", [True, False])
glpk_timeout = Integer("GLPK_TIMEOUT", default=60, bounds=[30, 90])
glpk_first_primal = Categorical("GLPK_FIRST_PRIMAL", [True, False])
glpk_reset_before_minimize = Categorical("GLPK_RESET_BEFORE_MINIMIZE", [True, False])
underflow_behavior = Categorical("UNDERFLOW_BEHAVIOR", [True, False])
skip_constraint_normalization = Categorical(
    "SKIP_CONSTRAINT_NORMALIZATION", [True, False]
)

nnenum_configspace.add_hyperparameters(
    [
        compress_init_box,
        eager_bounds,
        contract_zonotope,
        contract_zonotope_lp,
        contract_lp_optimized,
        contract_lp_track_witnesses,
        contract_lp_check_epsilon,
        overapprox_types,
        overapprox_near_root_max_splits,
        overapprox_types_near_root,
        overapprox_gen_limit_multiplier,
        overapprox_min_gen_limit,
        overapprox_lp_timeout,
        overapprox_both_bounds,
        branch_mode,
        try_quick_overapprox,
        quick_overapprox_types,
        split_order,
        result_save_polys_epsilon,
        split_tolerance,
        split_if_idle,
        shuffle_time,
        glpk_timeout,
        glpk_first_primal,
        glpk_reset_before_minimize,
        underflow_behavior,
        skip_constraint_normalization,
    ]
)

print(nnenum_configspace.sample_configuration())
