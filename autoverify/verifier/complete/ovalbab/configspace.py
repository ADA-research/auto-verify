"""OvalBab configspace."""

from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    Constant,
    Float,
    Integer,
)

OvalBabConfigspace = ConfigurationSpace(name="ovalbab")
OvalBabConfigspace.add_hyperparameters(
    [
        # bounding net1 ########################################################
        Constant(
            "bounding__nets1__bounding_algorithm",
            "propagation",
        ),
        Integer(
            "bounding__nets1__params__nb_steps",
            (1, 10),
            default=5,
        ),
        Float(
            "bounding__nets1__params__initial_step_size",
            (1e-1, 1e1),
            default=1e0,
        ),
        Float(
            "bounding__nets1__params__step_size_decay",
            (0.9, 1.0),
            default=0.98,
        ),
        Categorical(
            "bounding__nets1__params__joint_ib",
            [False],
            default=False,
        ),
        Categorical(  # TODO: Values
            "bounding__nets1__type",
            ["alpha-crown", "beta-crown"],
            default="beta-crown",
        ),
        Categorical(
            "bounding__nets1__auto_iters",
            [True, False],
            default=True,
        ),
        Integer(
            "bounding__nets1__batch_size",
            (25000, 75000),
            default=50000,
        ),
        Integer(
            "bounding__nets1__max_solver_batch",
            (250000, 750000),
            default=500000,
        ),
        # bounding net2 ########################################################
        Constant(
            "bounding__nets2__bounding_algorithm",
            "dual-anderson",
        ),
        Categorical(  # TODO: Values
            "bounding__nets2__params__bigm",
            ["init"],
            default="init",
        ),
        Categorical(  # TODO: Values
            "bounding__nets2__params__cut",
            ["only"],
            default="only",
        ),
        Categorical(  # TODO: Values
            "bounding__nets2__params__bigm_algorithm",
            ["adam"],
            default="adam",
        ),
        Integer(
            "bounding__nets2__params__nb_iter",
            (200, 1000),
            default=600,
        ),
        Integer(
            "bounding__nets2__params__cut_frequency",
            (150, 750),
            default=450,
        ),
        Integer(
            "bounding__nets2__params__max_cuts",
            (2, 22),
            default=12,
        ),
        Integer(
            "bounding__nets2__params__cut_add",
            (1, 4),
            default=2,
        ),
        Float(
            "bounding__nets2__params__initial_step_size",
            (1e-3, 1e-1),
            default=1e-2,
        ),
        Float(
            "bounding__nets2__params__final_step_size",
            (1e-6, 1e-3),
            default=1e-5,
        ),
        Integer(
            "bounding__nets2__params__init_params__nb_outer_iter",
            (500, 1500),
            default=1000,
        ),
        Float(
            "bounding__nets2__params__init_params__initial_step_size",
            (1e-3, 1e-1),
            default=1e-2,
        ),
        Float(
            "bounding__nets2__params__init_params__final_step_size",
            (1e-3, 1e-1),
            default=1e-2,
        ),
        Categorical(
            "bounding__nets2__params__init_params__larger_irl_if_naive_init",
            [True, False],
            default=True,
        ),
        Float(
            "bounding__nets2__params__restrict_factor",
            (0.5, 3.0),
            default=1.5,
        ),
        Categorical(
            "bounding__nets2__auto_iters",
            [True, False],
            default=True,
        ),
        Integer(
            "bounding__nets2__batch_size",
            (500, 1500),
            default=1000,
        ),
        Integer(
            "bounding__nets2__hard_overhead",
            (1, 20),
            default=10,
        ),
        # Bounding #############################################################
        Categorical(
            "bounding__do_ubs",
            [True, False],
            default=False,
        ),
        Integer(
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
            "ibs__use_lb",
            [True],
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
            default=False,
        ),
        Categorical(  # No bool constants...
            "ibs__joint_ib",
            [False],
            default=False,
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
            ["FSB", "SR"],
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
            ["KW__crown"],
            default="KW__crown",
        ),
        Categorical(
            "branching__bounding__type",  # TODO: values
            ["best_prop"],
            default="best_prop",
        ),
        Integer(
            "branching__bounding__max_solver_batch",
            (250000, 750000),
            default=500000,
        ),
    ]
)
