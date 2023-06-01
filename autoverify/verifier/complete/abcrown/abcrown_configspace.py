"""ab-crown configuration space."""

from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    Constant,
    EqualsCondition,
    Float,
    Integer,
)

AbCrownConfigspace = ConfigurationSpace()
AbCrownConfigspace.add_hyperparameters(
    [
        # general
        # Categorical(
        #     "general__device",
        #     ["cuda", "cpu"],
        #     default="cuda",
        # ),
        Categorical(
            "general__conv_mode",
            ["patches", "matrix"],
            default="patches",
        ),
        Categorical(
            "general__double_fp",
            [True, False],
            default=False,
        ),
        Categorical(
            "general__loss_reduction_func",
            ["sum", "min"],
            default="sum",
        ),
        Categorical(
            "general__sparse_alpha",
            [True, False],
            default=True,
        ),
        Categorical(
            "general__complete_verifier",
            ["bab", "mip", "bab_refine"],
            default="bab",
        ),
        Categorical(
            "general__enable_incomplete_verification",
            [True, False],
            default=True,
        ),
        # model - nothing
        # data - nothing
        # specification
        # ============================================================
        Categorical(
            "specification__type",
            ["lp", "bounds"],
            default="lp",
        ),
        Categorical(
            "specification__robustness_type",
            ["verified-acc", "runnerup"],  # "specify-target"],
            default="verified-acc",
        ),
        Categorical(
            "specification__norm",
            [1, 2, float("inf")],
            default=float("inf"),
        ),
        Categorical(
            "specification__epsilon",
            ["null"],
            default="null",
        ),
        # ============================================================
        # solver
        # Integer(
        #     "solver__batch_size",
        #     (1, 1000),
        #     default=64,
        # ),  # up to 500000..
        # Float(
        #     "solver__min_batch_size_ratio",
        #     (0.0, 1.0),
        #     default=0.1,
        # ),
        # NOTE: Fixing the batch size for now because of OOM errors. It is
        # instead a class attribute or passed as a param to verify_property`
        Constant(
            "solver__min_batch_size_ratio",
            0.1,
        ),
        Categorical(
            "solver__use_float64_in_last_iteration",
            [True, False],
            default=False,
        ),
        Integer(
            "solver__early_stop_patience",
            (1, 20),
            default=10,
        ),
        Float(
            "solver__start_save_best",
            (0.0, 1.0),
            default=0.5,
        ),
        Categorical(
            "solver__bound_prop_method",
            [
                "alpha-crown",
                "crown",
                "forward",
                "forward+crown",
                "alpha-forward",
                "crown-ibp",
                "init-crown",
            ],
            default="alpha-crown",
        ),
        Categorical(
            "solver__prune_after_crown",
            [False],
            default=False,
        ),
        Integer(
            "solver__crown__batch_size",
            (100_000_000, 10_000_000_000),
            default=1_000_000_000,
        ),
        Integer(
            "solver__crown__max_crown_size",
            (100_000_000, 10_000_000_000),
            default=1_000_000_000,
        ),
        Categorical(
            "solver__alpha-crown__alpha",
            [True, False],
            default=True,
        ),
        Float(
            "solver__alpha-crown__lr_alpha",
            (0.01, 0.2),
            default=0.1,
        ),
        Integer(
            "solver__alpha-crown__iteration",
            (1, 200),
            default=100,
        ),
        Categorical(
            "solver__alpha-crown__share_slopes",
            [True, False],
            default=False,
        ),
        Categorical(
            "solver__alpha-crown__no_joint_opt",
            [True, False],
            default=False,
        ),
        Float(
            "solver__alpha-crown__lr_decay",
            (0.9, 1.0),
            default=0.98,
        ),
        Categorical(
            "solver__alpha-crown__full_conv_alpha",
            [True, False],
            default=True,
        ),
        Float(
            "solver__beta-crown__lr_alpha",
            (0.01, 0.1),
            default=0.01,
        ),
        Float(
            "solver__beta-crown__lr_beta",
            (0.01, 0.2),
            default=0.05,
        ),
        Float(
            "solver__beta-crown__lr_decay",
            (0.9, 1.0),
            default=0.98,
        ),
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
        Categorical(
            "solver__forward__refine",
            [True, False],
            default=False,
        ),
        Categorical(
            "solver__forward__dynamic",
            [True, False],
            default=False,
        ),
        Integer(
            "solver__forward__max_dim",
            (1_000, 100_000),
            default=10_000,
        ),
        Constant(
            "solver__multi_class__multi_class_method",
            "allclass_domain",  # the rest are deprecated
        ),
        Integer(
            "solver__multi_class__label_batch_size",
            (1, 128),
            default=32,
        ),
        Categorical(
            "solver__multi_class__skip_with_refined_bound",
            [True, False],
            default=True,
        ),
        Categorical(
            "solver__mip__parallel_solvers",
            ["null"],
            default="null",
        ),
        Integer(
            "solver__mip__refine_neuron_timeout",
            (1, 30),
            default=15,
        ),
        Float(
            "solver__mip__refine_neuron_time_percentage",
            (0.0, 1.0),
            default=0.8,
        ),
        Categorical(
            "solver__mip__early_stop",
            [True, False],
            default=True,
        ),
        Categorical(
            "solver__mip__adv_warmup",
            [True, False],
            default=True,
        ),
        Constant(
            "solver__mip__mip_solver",
            "gurobi",
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
        # TODO: Enable once using cplex
        #
        # Float(
        #     "bab__cut__cplex_cuts_wait",
        #     (0, 2),
        #     default=0,
        # ),
        # Categorical(
        #     "bab__cut__cplex_cuts_revpickup",
        #     [True, False],
        #     default=True,
        # ),
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
        # bab-branching-attack
        # attack
        Categorical(
            "attack__pgd_order",
            ["before", "after"],
            default="before",
        ),
        Integer(
            "attack__pgd_steps",
            (1, 200),
            default=100,
        ),
        Integer(
            "attack__pgd_restarts",
            (1, 60),
            default=30,
        ),
        Categorical(
            "attack__pgd_early_stop",
            [True, False],
            default=True,
        ),
        Float(
            "attack__pgd_lr_decay",
            (0.9, 1.0),
            default=0.99,
        ),
        Categorical(
            "attack__pgd_alpha",
            ["auto"],
            default="auto",
        ),
        Categorical(
            "attack__pgd_loss_mode",
            ["null"],
            default="null",
        ),
        Categorical(
            "attack__enable_mip_attack",
            [True, False],
            default=False,
        ),
        Categorical(
            "attack__attack_mode",
            ["PGD", "GAMA"],
            default="PGD",
        ),
        Float(
            "attack__gama_lambda",
            (1.0, 20.0),
            default=1.0,
        ),
        Float(
            "attack__gama_decay",
            (0.8, 1.0),
            default=0.9,
        ),
        Categorical(
            "attack__check_clean",
            [True, False],
            default=False,
        ),
        Integer(
            "attack__input_split__pgd_steps",
            (1, 200),
            default=100,
        ),
        Integer(
            "attack__input_split__pgd_restarts",
            (1, 60),
            default=30,
        ),
        Categorical(
            "attack__input_split__pgd_alpha",
            ["auto"],
            default="auto",
        ),
        Integer(
            "attack__input_split_enhanced__pgd_steps",
            (1, 400),
            default=100,
        ),
        Integer(
            "attack__input_split_enhanced__pgd_restarts",
            (100000, 10000000),
            default=5000000,
        ),
        Categorical(
            "attack__input_split_enhanced__pgd_alpha",
            ["auto"],
            default="auto",
        ),
        Integer(
            "attack__input_split_check_adv__pgd_steps",
            (1, 400),
            default=100,
        ),
        Integer(
            "attack__input_split_check_adv__pgd_restarts",
            (100000, 10000000),
            default=5000000,
        ),
        Categorical(
            "attack__input_split_check_adv__pgd_alpha",
            ["auto"],
            default="auto",
        ),
    ]
)

AbCrownConfigspace.add_conditions(
    [
        EqualsCondition(
            AbCrownConfigspace.get_hyperparameter("solver__forward__dynamic"),
            AbCrownConfigspace.get_hyperparameter("specification__norm"),
            float("inf"),
        ),
        EqualsCondition(
            AbCrownConfigspace.get_hyperparameter(
                "bab__branching__input_split__enable"
            ),
            AbCrownConfigspace.get_hyperparameter(
                "general__enable_incomplete_verification"
            ),
            True,
        ),
        # EqualsCondition(
        #     AbCrownConfigspace.get_hyperparameter("bab__cut__cplex_cuts_wait"),
        #     AbCrownConfigspace.get_hyperparameter("bab__cut__cplex_cuts"),
        #     True,
        # ),
        # EqualsCondition(
        #     AbCrownConfigspace.get_hyperparameter(
        #         "bab__cut__cplex_cuts_revpickup"
        #     ),
        #     AbCrownConfigspace.get_hyperparameter("bab__cut__cplex_cuts"),
        #     True,
        # ),
    ]
)
