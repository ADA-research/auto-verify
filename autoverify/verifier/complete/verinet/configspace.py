"""_summary_."""

from ConfigSpace import Categorical, ConfigurationSpace, Float, Integer

VerinetConfigspace = ConfigurationSpace(name="verinet")
VerinetConfigspace.add_hyperparameters(
    [
        Categorical(
            "PRECISION",
            [32, 64],
            default=32,
        ),
        Integer(
            "QUEUE_DEPTH",
            (1, 10),
            default=1,
        ),
        Integer(
            "MAX_CHILDREN_SUSPEND_TIME",
            (300, 900),
            default=600,
        ),
        Integer(
            "MAX_ACCEPTED_MEMORY_INCREASE",
            (10, 30),
            default=20,
        ),
        Categorical(
            "USE_ONE_SHOT_ATTEMPT",
            [True, False],
            default=True,
        ),
        Categorical(
            "USE_PRE_PROCESSING_ATTACK",
            [True, False],
            default=True,
        ),
        # Categorical(
        #     "MAX_QUEUED_BRANCHES",
        #     [True, False],
        #     default=True,
        # ),
        Integer(
            "MAX_ESTIMATED_MEM_USAGE",
            (64 * 10**8, 64 * 10**11),
            default=64 * 10**9,
        ),
        Integer(
            "OPTIMISED_RELU_RELAXATION_MAX_BOUNDS_MULTIPLIER",
            (1, 3),
            default=2,
        ),
        Categorical(
            "USE_SSIP",
            [True, False],
            default=False,
        ),
        Categorical(
            "STORE_SSIP_BOUNDS",
            [True, False],
            default=False,
        ),
        Categorical(
            "INPUT_NODE_SPLIT",
            [True, False],
            default=True,
        ),
        Categorical(
            "HIDDEN_NODE_SPLIT",
            [True, False],
            default=True,
        ),
        Float(
            "INDIRECT_HIDDEN_MULTIPLIER",
            (0.5, 1.0),
            default=0.75,
        ),
        Float(
            "INDIRECT_INPUT_MULTIPLIER",
            (0.5, 1.0),
            default=0.75,
        ),
        Categorical(
            "USE_BIAS_SEPARATED_CONSTRAINTS",
            [True, False],
            default=True,
        ),
        Categorical(
            "PERFORM_LP_MAXIMISATION",
            [True, False],
            default=False,
        ),
        Categorical(
            "USE_OPTIMISED_RELAXATION_CONSTRAINTS",
            [True, False],
            default=True,
        ),
        Categorical(
            "USE_OPTIMISED_RELAXATION_SPLIT_HEURISTIC",
            [True, False],
            default=True,
        ),
        Categorical(
            "USE_SIMPLE_LP",
            [True, False],
            default=True,
        ),
        Integer(
            "NUM_ITER_OPTIMISED_RELAXATIONS",
            (1, 5),
            default=3,
        ),
        Categorical(
            "USE_LP_PRESOLVE",
            [0, 1],
            default=0,
        ),
        Integer(
            "GRADIENT_DESCENT_INTERVAL",
            (1, 5),
            default=1,
        ),
        Integer(
            "GRADIENT_DESCENT_MAX_ITERS",
            (1, 10),
            default=5,
        ),
        Float(
            "GRADIENT_DESCENT_STEP",
            (0.01, 0.2),
            default=0.1,
        ),
        Float(
            "GRADIENT_DESCENT_MIN_LOSS_CHANGE",
            (1e-3, 1e-1),
            default=1e-2,
        ),
    ]
)
