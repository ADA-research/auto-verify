"""OvalBab configspace."""

from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    Constant,
    Float,
    Integer,
)

# TODO: bounding nets is a list?
OvalBabConfigspace = ConfigurationSpace()
OvalBabConfigspace.add_hyperparameters(
    [
        # Bounding #############################################################
        Categorical(
            "bounding__do_ubs",
            [True, False],
            default=True,
        ),
        Categorical(
            "bounding__batch_size",
            (1, 2000),
            default=1000,
        ),
        Categorical(
            "bounding__parent_init",
            [True, False],
            default=True,
        ),
        # IBS ##################################################################
        Categorical(
            "ibs__use_ib",
            [True, False],
            default=True,
        ),
        Categorical(  # TODO:  other values
            "ibs__tight_ib",
            ["null"],
            default="null",
        ),
        Categorical(
            "ibs__fixed_ib",
            [True, False],
            default=True,
        ),
        Categorical(
            "ibs__joint_ib",
            [True, False],
            default=True,
        ),
        # upper_bounding #######################################################
        Categorical(  # TODO: other values
            "upper_bounding__ub_method",
            ["mi_fgsm"],
            default="mi_fgsm",
        ),
        Integer(
            "upper_bounding__adv_params__iters",
            (250, 750),
            default=500,
        ),
        Categorical(
            "upper_bounding__adv_params__lr_tensor",
            [True, False],
            default=True,
        ),
        Integer(
            "upper_bounding__adv_params__num_adv_ex",
            (50, 150),
            default=100,
        ),
        Integer(  # TODO: Values
            "upper_bounding__adv_params__check_adv",
            (1, 3),
            default=2,
        ),
        Categorical(
            "upper_bounding__adv_params__mu_tensor",
            [True, False],
            default=True,
        ),
        Categorical(
            "upper_bounding__adv_params__decay_tensor",
            [True, False],
            default=True,
        ),
        # branching ############################################################
        Categorical(  # TODO: values
            "branching__heuristic_type",
            ["FSB"],
            default="FSB",
        ),
        Integer(
            "branching__max_domains",
            (25000, 750000),
            default=50000,
        ),
        Categorical(
            "branching__bounding__bounding_algorithm",
            ["propagation"],
            default="propagation",
        ),
        Categorical(  # TODO: params
            "branching__bounding__params__best_among",
            ["KW-crown"],
            default="KW-crown",
        ),
        Categorical(
            "branching__type",  # TODO: values
            ["best_prop"],
            default="best_prop",
        ),
        Integer(
            "branching__max_solver_batch",
            (250000, 750000),
            default=500000,
        ),
    ]
)
