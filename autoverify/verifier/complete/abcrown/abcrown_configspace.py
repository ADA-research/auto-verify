"""ab-crown configuration space."""
from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    Constant,
    Float,
    Integer,
)

AbCrownConfigspace = ConfigurationSpace()

AbCrownConfigspace.add_hyperparameters(
    [
        Categorical(
            "general__complete_verifier",
            ["bab", "mip", "bab_refine"],
            default="bab",
        ),
        Integer(
            "solver__batch_size",
            (1, 1000),
            default=64,
        ),  # up to 500000..
        Float(
            "solver__beta-crown__lr_decay",
            (0.9, 1.0),
            default=0.98,
        ),
        # TODO: Havent found if there are options besides adam
        Categorical(
            "solver__beta-crown__optimizer",
            ["adam"],
            default="adam",
        ),
        Integer(
            "solver__beta-crown__iteration",
            (1, 100),
            default=50,
        ),
        Categorical(
            "solver__beta-crown__enable_opt_interm_bounds",
            [True, False],
            default=False,
        ),
        Categorical(
            "solver__beta-crown__all_node_split_LP",
            [True, False],
            default=False,
        ),
        # bab
        Categorical(
            "bab__pruning_in_iteration",
            [True, False],
            default=True,
        ),
        Float(
            "bab__pruning_in_iteration_ratio",
            (0.0, 1.0),
            default=0.2,
        ),
        Categorical(
            "bab__sort_targets",
            [True, False],
            default=False,
        ),
        Categorical(
            "bab__batched_domain_list",
            [True, False],
            default=True,
        ),
        Categorical(
            "bab__cut__enabled",
            [True, False],
            default=False,
        ),
        Categorical(
            "bab__cut__bab_cut",
            [True, False],
            default=False,
        ),
        Constant(
            "bab__cut__method",
            "null",
        ),
        Float(
            "bab__cut__lr",
            (0.001, 0.2),
            default=0.01,
        ),
        Float(
            "bab__cut__lr_decay",
            (0.9, 1.0),
            default=1.0,
        ),
        Integer(
            "bab__cut__iteration",
            (10, 200),
            default=100,
        ),
        Constant(
            "bab__cut__bab_iteration",
            -1,
        ),
        Float(
            "bab__cut__lr_beta",
            (0.001, 0.2),
            default=0.02,
        ),
        Integer(
            "bab__cut__number_cuts",
            (1, 100),
            default=50,
        ),
        Integer(
            "bab__cut__topk_cuts_in_filter",
            (1, 200),
            default=100,
        ),
        Integer(
            "bab__cut__batch_size_primal",
            (1, 200),
            default=100,
        ),
        Integer(
            "bab__cut__max_num",
            (100_000_000, 10_000_000_000),
            default=1_000_000_000,
        ),
        Categorical(
            "bab__cut__patches_cut",
            [True, False],
            default=False,
        ),
        Categorical(
            "bab__cut__cplex_cuts",
            [False],  # [True, False], # TODO: Use cplex?
            default=False,
        ),
        Float(
            "bab__cut__cplex_cuts_wait",
            (0, 2),
            default=0,
        ),
        Categorical(
            "bab__cut__cplex_cuts_revpickup",
            [True, False],
            default=True,
        ),
        Categorical(
            "bab__cut__cut_reference_bounds",
            [True, False],
            default=True,
        ),
        Categorical(
            "bab__cut__fix_intermediate_bounds",
            [True, False],
            default=False,
        ),
        Categorical(
            "bab__branching__method",
            [
                "babsr",
                "fsb",
                "kfsb",
                "sb",
                "kfsb-intercept-only",
                "naive",
            ],
            default="kfsb",
        ),
        Integer(
            "bab__branching__candidates",
            (1, 10),
            default=3,
        ),
        Categorical(
            "bab__branching__reduceop",
            ["min", "max", "mean", "auto"],
            default="min",
        ),
        Float(
            "bab__branching__sb_coeff_thresh",
            (0.000_01, 0.001),
            default=0.001,
        ),
        Categorical(
            "bab__branching__input_split__enable",
            [True, False],
            default=False,
        ),
        Categorical(  # noqa: E501
            "bab__branching__input_split__enhanced_bound_prop_method",
            ["alpha-crown", "crown", "forward+crown", "crown-ibp"],
            default="alpha-crown",
        ),
        Categorical(  # noqa: E501
            "bab__branching__input_split__enhanced_branching_method",
            ["naive", "sb"],
            default="naive",
        ),
        Float(
            "bab__branching__input_split__enhanced_bound_patience",
            (10_000_000.0, 1_000_000_000.0),
            default=100_000_000.0,
        ),
        Float(
            "bab__branching__input_split__attack_patience",
            (10_000_000.0, 1_000_000_000.0),
            default=100_000_000.0,
        ),
        Integer(
            "bab__branching__input_split__adv_check",
            (0, 10),
            default=-0,
        ),
        Integer(
            "bab__branching__input_split__sort_domain_interval",
            (-1, 10),
            default=-1,
        ),
    ]
)


# AbCrownConfigspace.config_spaces[ConfigurationLevel.verifier].add_conditions(
#     [
#         EqualsCondition(
#             AbCrownConfigspace.get_parameter("solver__forward__dynamic"),
#             AbCrownConfigspace.get_parameter("specification__norm"),
#             float("inf"),
#         )
#     ]
# )
