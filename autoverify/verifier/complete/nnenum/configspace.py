"""_summary_."""
from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    EqualsCondition,
    Float,
    Integer,
)

NnenumConfigspace = ConfigurationSpace(name="nnenum")
# NnenumConfigspace.add_hyperparameters(
#     [
#         # https://github.com/stanleybak/nnenum/blob/55363ce71bb047f02dec1be0d4d58526c737ff53/src/nnenum/nnenum.py#LL150C25-L150C29
#         Categorical(
#             "settings_mode",
#             ["auto", "control", "image", "exact"],
#             default="auto",
#         ),
#     ]
# )
NnenumConfigspace.add_hyperparameters(
    [
        Categorical(
            "SINGLE_SET",
            [True, False],
            default=False,
        ),
        Categorical(
            "COMPRESS_INIT_BOX",
            [True, False],
            default=True,
        ),
        Categorical(
            "EAGER_BOUNDS",
            [True, False],
            default=True,
        ),
        Categorical(
            "CONTRACT_ZONOTOPE",
            [True, False],
            default=False,
        ),
        Categorical(
            "CONTRACT_ZONOTOPE_LP",
            [True, False],
            default=True,
        ),
        Categorical(
            "CONTRACT_LP_OPTIMIZED",
            [True, False],
            default=True,
        ),
        Categorical(
            "CONTRACT_LP_TRACK_WITNESSES",
            [True, False],
            default=True,
        ),
        # Categorical(
        #     "OVERAPPROX_TYPES",
        # ),
        Integer(
            "OVERAPPROX_NEAR_ROOT_MAX_SPLITS",
            (1, 5),
            default=2,
        ),
        Float(
            "OVERAPPROX_GEN_LIMIT_MULTIPLIER",
            (0.0, 3.0),
            default=1.5,
        ),
        Categorical(
            "INF_OVERAPPROX_MIN_GEN_LIMIT",
            [True, False],
            default=False,
        ),
        Integer(
            "OVERAPPROX_MIN_GEN_LIMIT",
            (1, 100),
            default=50,
        ),
        Categorical(
            "INF_OVERAPPROX_LP_TIMEOUT",
            [True, False],
            default=False,
        ),
        Float(
            "OVERAPPROX_LP_TIMEOUT",
            (0.0, 5.0),
            default=1.0,
        ),
        Categorical(
            "OVERAPPROX_BOTH_BOUNDS",
            [True, False],
            default=False,
        ),
        Categorical(
            "BRANCH_MODE",
            # branch_overapprox, branch_ego, branch_ego_light, branch_exact
            [0, 1, 2, 3],
            default=0,
        ),
        Categorical(
            "TRY_QUICK_OVERAPPROX",
            [True, False],
            default=True,
        ),
        Categorical(
            "SPLIT_ORDER",
            # split_largest, split_one_norm, split_smallest, split_inorder
            [0, 1, 2, 3],
            default=1,
        ),
        Categorical(
            "OFFLOAD_CLOSEST_TO_ROOT",
            [True, False],
            default=True,
        ),
        Float(
            "SPLIT_TOLERANCE",
            (1e-9, 1e-7),
            default=1e-8,
        ),
        Categorical(
            "SPLIT_IF_IDLE",
            [True, False],
            default=True,
        ),
        Integer(
            "GLPK_TIMEOUT",
            (10, 120),
            default=60,
        ),
        Categorical(
            "GLPK_FIRST_PRIMAL",
            [True, False],
            default=True,
        ),
        Categorical(
            "GLPK_RESET_BEFORE_MINIMIZE",
            [True, False],
            default=False,
        ),
        Categorical(
            "SKIP_COMPRESSED_CHECK",
            [True, False],
            default=False,
        ),
        Categorical(
            "SKIP_CONSTRAINT_NORMALIZATION",
            [True, False],
            default=False,
        ),
    ]
)

NnenumConfigspace.add_conditions(
    [
        EqualsCondition(
            NnenumConfigspace["OVERAPPROX_MIN_GEN_LIMIT"],
            NnenumConfigspace["INF_OVERAPPROX_MIN_GEN_LIMIT"],
            False,
        ),
        EqualsCondition(
            NnenumConfigspace["OVERAPPROX_LP_TIMEOUT"],
            NnenumConfigspace["INF_OVERAPPROX_LP_TIMEOUT"],
            False,
        ),
    ]
)
