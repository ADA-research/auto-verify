"""ab-crown configuration space."""

from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    Constant,
    EqualsCondition,
    Float,
    ForbiddenAndConjunction,
    ForbiddenEqualsClause,
    InCondition,
    Integer,
    NotEqualsCondition,
)

AbCrownConfigspace = ConfigurationSpace(name="abcrown")
AbCrownConfigspace.add_hyperparameters(
    [
        ########################################################################
        # GENERAL
        ########################################################################
        Categorical(
            "general__complete_verifier",
            ["bab", "mip", "bab-refine", "skip"],
            default="bab",
        ),
        Categorical(
            "general__enable_incomplete_verification",
            [True, False],
            default=True,
        ),
        Categorical(
            "general__loss_reduction_func",
            ["sum", "min", "max"],
            default="sum",
        ),
        ########################################################################
        # SOLVER
        ########################################################################
        # Integer(
        #     "solver__early_stop_patience",
        #     (1, 30),
        #     default=10,
        # ),
        # Float(
        #     "solver__start_save_best",
        #     (0.0, 1.0),
        #     default=0.5,
        # ),
        Categorical(
            "solver__bound_prop_method",
            [
                "alpha-crown",
                "crown",
                "forward",
                "forward+crown",
                "alpha-forward",
                "init-crown",
            ],
            default="alpha-crown",
        ),
        # Categorical(
        #     "solver__prune_after_crown",
        #     [True, False],
        #     default=False,
        # ),
        # Categorical(
        #     "solver__alpha-crown__alpha",
        #     [True, False],
        #     default=True,
        # ),
        # Float(
        #     "solver__alpha-crown__lr_alpha",
        #     (0.001, 0.2),
        #     default=0.1,
        #     log=True,
        # ),
        # Integer(
        #     "solver__alpha-crown__iteration",
        #     (1, 200),
        #     default=100,
        # ),
        # Categorical(
        #     "solver__alpha-crown__share_slopes",
        #     [True, False],
        #     default=False,
        # ),
        # Categorical(
        #     "solver__alpha-crown__no_joint_opt",
        #     [True, False],
        #     default=False,
        # ),
        # Float(
        #     "solver__alpha-crown__lr_decay",
        #     (0.95, 1.0),
        #     default=0.98,
        #     log=True,
        # ),
        # Categorical(
        #     "solver__alpha-crown__full_conv_alpha",
        #     [True, False],
        #     default=True,
        # ),
        # Float(
        #     "solver__beta-crown__lr_alpha",
        #     (0.01, 0.1),
        #     default=0.01,
        # ),
        # Float(
        #     "solver__beta-crown__lr_beta",
        #     (0.01, 0.2),
        #     default=0.05,
        #     log=True,
        # ),
        # Float(
        #     "solver__beta-crown__lr_decay",
        #     (0.95, 1.0),
        #     default=0.98,
        #     log=True,
        # ),
        # Constant(
        #     "solver__beta-crown__optimizer",
        #     "adam",
        # ),
        # Integer(
        #     "solver__beta-crown__iteration",
        #     (1, 100),
        #     default=50,
        # ),
        # Categorical(  # TODO: Only with mip refine
        #     "solver__beta-crown__enable_opt_interm_bounds",
        #     [True, False],
        #     default=False,
        # ),
        # Categorical(
        #     "solver__beta-crown__all_node_split_LP",
        #     [True, False],
        #     default=False,
        # ),
        # Categorical(
        #     "solver__forward__refine",
        #     [True, False],
        #     default=False,
        # ),
        # Categorical(
        #     "solver__forward__dynamic",
        #     [True, False],
        #     default=False,
        # ),
        # Categorical(
        #     "solver__multi_class__skip_with_refined_bound",
        #     [True, False],
        #     default=True,
        # ),
        # Categorical(
        #     "solver__mip__adv_warmup",
        #     [True, False],
        #     default=True,
        # ),
        ########################################################################
        # BAB
        ########################################################################
        # Categorical(
        #     "bab__pruning_in_iteration",
        #     [True, False],
        #     default=True,
        # ),
        # Float(
        #     "bab__pruning_in_iteration_ratio",
        #     (0.01, 1.0),
        #     default=0.2,
        #     log=True,
        # ),
        # Categorical(
        #     "bab__sort_targets",
        #     [True, False],
        #     default=False,
        # ),
        # Categorical(
        #     "bab__batched_domain_list",
        #     [True, False],
        #     default=True,
        # ),
        # Categorical(
        #     "bab__cut__enabled",
        #     [True, False],
        #     default=False,
        # ),
        # Categorical(
        #     "bab__cut__bab_cut",
        #     [True, False],
        #     default=False,
        # ),
        # Float(
        #     "bab__cut__lr",
        #     (0.001, 0.2),
        #     default=0.01,
        #     log=True,
        # ),
        # Float(
        #     "bab__cut__lr_decay",
        #     (0.9, 1.0),
        #     default=1.0,
        #     log=True,
        # ),
        # Integer(
        #     "bab__cut__iteration",
        #     (10, 200),
        #     default=100,
        # ),
        # Constant(
        #     "bab__cut__bab_iteration",
        #     -1,
        # ),
        # Float(
        #     "bab__cut__lr_beta",
        #     (0.001, 0.2),
        #     default=0.02,
        #     log=True,
        # ),
        # Integer(
        #     "bab__cut__number_cuts",
        #     (1, 100),
        #     default=50,
        # ),
        # Integer(
        #     "bab__cut__topk_cuts_in_filter",
        #     (1, 200),
        #     default=100,
        # ),
        Categorical(
            "bab__branching__method",
            [
                "kfsb",
                "babsr",
                "fsb",
                # "sb", # doesnt support relu split
                "kfsb-intercept-only",
                # "naive", # doesnt support relu split
            ],
            default="kfsb",
        ),
        # Integer(
        #     "bab__branching__candidates",
        #     (1, 10),
        #     default=3,
        # ),
        Categorical(
            "bab__branching__reduceop",
            ["min", "max"],
            default="min",
        ),
        Categorical(
            "bab__branching__input_split__enable",
            [True, False],
            default=False,
        ),
        Categorical(
            "bab__branching__input_split__enhanced_bound_prop_method",
            ["alpha-crown", "crown", "forward+crown", "crown-ibp"],
            default="alpha-crown",
        ),
        Categorical(
            "bab__branching__input_split__enhanced_branching_method",
            ["naive", "sb"],
            default="naive",
        ),
        Float(
            "bab__branching__input_split__enhanced_bound_patience",
            (10, 120),
            default=30,
        ),
        Float(
            "bab__branching__input_split__attack_patience",
            (10, 120),
            default=80,
        ),
        # Integer(
        #     "bab__branching__input_split__adv_check",
        #     (0, 10),
        #     default=-0,
        # ),
        # Integer(
        #     "bab__branching__input_split__sort_domain_interval",
        #     (-1, 10),
        #     default=-1,
        # ),
        # Constant(  # TODO: Find out how this works
        #     "bab__attack__enabled",
        #     False,
        # ),
        ########################################################################
        # ATTACK
        ########################################################################
        Categorical(
            "attack__pgd_order",
            ["before", "middle", "after", "skip"],
            default="before",
        ),
        # Integer(
        #     "attack__pgd_steps",
        #     (1, 200),
        #     default=100,
        # ),
        # Integer(
        #     "attack__pgd_restarts",
        #     (1, 60),
        #     default=30,
        # ),
        # Categorical(
        #     "attack__pgd_early_stop",
        #     [True, False],
        #     default=True,
        # ),
        # Float(
        #     "attack__pgd_lr_decay",
        #     (0.9, 1.0),
        #     default=0.99,
        # ),
        # Categorical(
        #     "attack__pgd_alpha",
        #     ["auto"],
        #     default="auto",
        # ),
        # Categorical(
        #     "attack__pgd_loss_mode",
        #     ["null"],
        #     default="null",
        # ),
        Categorical(
            "attack__enable_mip_attack",
            [True, False],
            default=False,
        ),
        Categorical(
            "attack__attack_mode",
            ["diversed_PGD", "diversed_GAMA_PGD", "PGD", "boundary"],
            default="PGD",
        ),
        # Float(
        #     "attack__gama_lambda",
        #     (1.0, 20.0),
        #     default=1.0,
        # ),
        # Float(
        #     "attack__gama_decay",
        #     (0.8, 1.0),
        #     default=0.9,
        # ),
        # Categorical(
        #     "attack__check_clean",
        #     [True, False],
        #     default=False,
        # ),
        # Integer(
        #     "attack__input_split__pgd_steps",
        #     (1, 200),
        #     default=100,
        # ),
        # Integer(
        #     "attack__input_split__pgd_restarts",
        #     (1, 60),
        #     default=30,
        # ),
        # Categorical(
        #     "attack__input_split__pgd_alpha",
        #     ["auto"],
        #     default="auto",
        # ),
        # Integer(
        #     "attack__input_split_enhanced__pgd_steps",
        #     (1, 400),
        #     default=100,
        # ),
        # Integer(
        #     "attack__input_split_enhanced__pgd_restarts",
        #     (1, 100),
        #     default=50,
        # ),
        # Categorical(
        #     "attack__input_split_enhanced__pgd_alpha",
        #     ["auto"],
        #     default="auto",
        # ),
        # Integer(
        #     "attack__input_split_check_adv__pgd_steps",
        #     (1, 400),
        #     default=100,
        # ),
        # Integer(
        #     "attack__input_split_check_adv__pgd_restarts",
        #     (1, 100),
        #     default=50,
        # ),
        # Categorical(
        #     "attack__input_split_check_adv__pgd_alpha",
        #     ["auto"],
        #     default="auto",
        # ),
    ]
)

AbCrownConfigspace.add_conditions(
    [
        # EqualsCondition(
        #     AbCrownConfigspace[
        #         "bab__branching__input_split__enhanced_bound_prop_method"
        #     ],
        #     AbCrownConfigspace["bab__branching__input_split__enable"],
        #     True,
        # ),
        NotEqualsCondition(
            AbCrownConfigspace["attack__attack_mode"],
            AbCrownConfigspace["attack__pgd_order"],
            "skip",
        ),
        # EqualsCondition(
        #     AbCrownConfigspace["bab__cut__enabled"],
        #     AbCrownConfigspace["general__enable_incomplete_verification"],
        #     True,
        # ),
        # InCondition(
        #     AbCrownConfigspace["solver__beta-crown__enable_opt_interm_bounds"],
        #     AbCrownConfigspace["general__complete_verifier"],
        #     ["mip", "bab-refine"],
        # ),
        # EqualsCondition(
        #     AbCrownConfigspace["bab__pruning_in_iteration_ratio"],
        #     AbCrownConfigspace["bab__pruning_in_iteration"],
        #     True,
        # ),
        # InCondition(
        #     AbCrownConfigspace["bab__branching__candidates"],
        #     AbCrownConfigspace["bab__branching__method"],
        #     ["kfsb"],
        # ),
    ]
)

for hp in AbCrownConfigspace.get_hyperparameters():
    if not hp.name.startswith("bab__branching__input_split"):
        continue

    if hp.name == "bab__branching__input_split__enable":
        continue

    AbCrownConfigspace.add_condition(
        EqualsCondition(
            hp, AbCrownConfigspace["bab__branching__input_split__enable"], True
        )
    )

for hp in AbCrownConfigspace.get_hyperparameters():
    if not hp.name.startswith("attack__"):
        continue

    if hp.name == "attack__pgd_order":
        continue

    AbCrownConfigspace.add_condition(
        NotEqualsCondition(hp, AbCrownConfigspace["attack__pgd_order"], "skip")
    )


AbCrownConfigspace.add_forbidden_clauses(
    [
        # ForbiddenAndConjunction(
        #     ForbiddenEqualsClause(
        #         AbCrownConfigspace["bab__attack__enabled"], True
        #     ),
        #     ForbiddenEqualsClause(
        #         AbCrownConfigspace["general__enable_incomplete_verification"],
        #         False,
        #     ),
        # ),
        ForbiddenAndConjunction(
            ForbiddenEqualsClause(
                AbCrownConfigspace["general__enable_incomplete_verification"],
                True,
            ),
            ForbiddenEqualsClause(
                AbCrownConfigspace["bab__branching__input_split__enable"], True
            ),
        ),
        ForbiddenAndConjunction(
            ForbiddenEqualsClause(
                AbCrownConfigspace["general__complete_verifier"], "skip"
            ),
            ForbiddenEqualsClause(
                AbCrownConfigspace["general__enable_incomplete_verification"],
                False,
            ),
            ForbiddenEqualsClause(
                AbCrownConfigspace["attack__pgd_order"], "skip"
            ),
        ),
    ]
)
