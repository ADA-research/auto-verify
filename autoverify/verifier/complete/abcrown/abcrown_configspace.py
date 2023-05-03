"""_summary_."""
from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    Constant,
    Float,
    Integer,
)

from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)

AbCrownConfigspace = VerifierConfigurationSpace(
    {
        ConfigurationLevel.SOLVER: ConfigurationSpace(
            space={"uniform_integer_solver": (1, 10)}
        ),
        # TODO: Remove parameters irrelevant to performance
        ConfigurationLevel.VERIFIER: ConfigurationSpace(
            name="abcrown_verifier",
            space={
                # general
                "general__device": Categorical(
                    "general__device",
                    ["cuda", "cpu"],
                    default="cuda",
                ),
                "general__seed": Integer(
                    "general__seed",
                    (0, 100),
                    default=100,
                ),
                "general__conv_mode": Categorical(
                    "general__conv_mode",
                    ["patches", "matrix"],
                    default="patches",
                ),
                "general__double_fp": Categorical(
                    "general__double_fp",
                    [True, False],
                    default=False,
                ),
                "general__loss_reduction_func": Categorical(
                    "general__loss_reduction_func",
                    ["sum", "min"],
                    default="sum",
                ),
                "general__sparse_alpha": Categorical(
                    "general__sparse_alpha",
                    [True, False],
                    default=True,
                ),
                "general__save_adv_example": Categorical(
                    "general__save_adv_example",
                    [True, False],
                    default=False,
                ),
                "general__precompile_jit": Categorical(
                    "general__precompile_jit",
                    [True, False],
                    default=False,
                ),
                # TODO: default
                "general__complete_verifier": Categorical(
                    "general__complete_verifier",
                    ["bab", "mip", "bab_refine"],
                ),
                "general__enable_incomplete_verification": Categorical(
                    "general__enable_incomplete_verification",
                    [True, False],
                    default=True,
                ),
                "general__csv_name": Categorical(
                    "general__csv_name",
                    [True, False],
                    default=False,
                ),
                "general__result_file": Categorical(
                    "general__result_file",
                    [True, False],
                    default=False,
                ),
                "general__root_path": Categorical(
                    "general__root_path",
                    [True, False],
                    default=False,
                ),
                # model - nothing
                # data - nothing
                # specification
                "specification__type": Categorical(
                    "specification__type",
                    ["lp", "bounds"],
                    default="lp",
                ),
                "specification__robustness_type": Categorical(
                    "specification__robustness_type",
                    ["verified-acc", "runnerup", "specify-target"],
                    default="verified-acc",
                ),
                "specification__norm": Categorical(
                    "specification__norm",
                    ["1", "2", ".inf"],
                    default=".inf",
                ),
                "specification__epsilon": Categorical(
                    "specification__epsilon",
                    ["null"],
                    default="null",
                ),
                # solver
                "solver__batch_size": Integer(
                    "solver__batch_size",
                    (1, 1000),
                    default=64,
                ),  # up to 500000..
                "solver__min_batch_size_ratio": Float(
                    "solver__min_batch_size_ratio",
                    (0.0, 1.0),
                    default=0.1,
                ),
                "solver__use_float64_in_last_iteration": Categorical(
                    "solver__use_float64_in_last_iteration",
                    [True, False],
                    default=False,
                ),
                "solver__early_stop_patience": Integer(
                    "solver__early_stop_patience",
                    (1, 20),
                    default=10,
                ),
                "solver__start_save_best": Float(
                    "solver__start_save_best",
                    (0.0, 1.0),
                    default=0.5,
                ),
                # TODO: Options for bound_prop_method?
                "solver__bound_prop_method": Categorical(
                    "solver__bound_prop_method",
                    ["alpha-crown"],
                    default="alpha-crown",
                ),
                "solver__prune_ater_crown": Categorical(
                    "solver__prune_ater_crown",
                    [True, False],
                    default=False,
                ),
                "solver__crown__batch_size": Integer(
                    "solver__crown__batch_size",
                    (100_000_000, 10_000_000_000),
                    default=1_000_000_000,
                ),
                "solver__crown__max_crown_size": Integer(
                    "solver__crown__max_crown_size",
                    (100_000_000, 10_000_000_000),
                    default=1_000_000_000,
                ),
                "solver__alpha-crown__alpha": Categorical(
                    "solver__alpha-crown__alpha",
                    [True, False],
                    default=True,
                ),
                "solver__alpha-crown__lr_alpha": Float(
                    "solver__alpha-crown__lr_alpha",
                    (0.01, 0.2),
                    default=0.1,
                ),
                "solver__alpha-crown__iteration": Integer(
                    "solver__alpha-crown__iteration",
                    (1, 200),
                    default=100,
                ),
                "solver__alpha-crown__share_slopes": Categorical(
                    "solver__alpha-crown__share_slopes",
                    [True, False],
                    default=False,
                ),
                "solver__alpha-crown__no_join_opt": Categorical(
                    "solver__alpha-crown__no_join_opt",
                    [True, False],
                    default=False,
                ),
                "solver__alpha-crown__lr_decay": Float(
                    "solver__alpha-crown__lr_decay",
                    (0.9, 1.0),
                    default=0.98,
                ),
                "solver__alpha-crown__full_conv_alpha": Categorical(
                    "solver__alpha-crown__full_conv_alpha",
                    [True, False],
                    default=True,
                ),
                "solver__beta_crown__lr_alpha": Float(
                    "solver__beta_crown__lr_alpha",
                    (0.01, 0.1),
                    default=0.01,
                ),
                "solver__beta_crown__lr_beta": Float(
                    "solver__beta_crown__lr_beta",
                    (0.01, 0.2),
                    default=0.05,
                ),
                "solver__beta-crown__lr_decay": Float(
                    "solver__beta-crown__lr_decay",
                    (0.9, 1.0),
                    default=0.98,
                ),
                # TODO: Options for beta-crown__optimizer
                "solver__beta-crown__optimizer": Categorical(
                    "solver__beta-crown__optimizer",
                    ["adam"],
                    default="adam",
                ),
                "solver__beta-crown__iteration": Integer(
                    "solver__beta-crown__iteration",
                    (1, 100),
                    default=50,
                ),
                "solver__beta-crown__enable_opt_interm_bounds": Categorical(
                    "solver__beta-crown__enable_opt_interm_bounds",
                    [True, False],
                    default=False,
                ),
                "solver__beta-crown__all_node_split_LP": Categorical(
                    "solver__beta-crown__all_node_split_LP",
                    [True, False],
                    default=False,
                ),
                "solver__forward__refine": Categorical(
                    "solver__forward__refine",
                    [True, False],
                    default=False,
                ),
                "solver__forward__dynamic": Categorical(
                    "solver__forward__dynamic",
                    [True, False],
                    default=False,
                ),
                "solver__forward__max_dim": Integer(
                    "solver__forward__max_dim",
                    (1_000, 100_000),
                    default=10_000,
                ),
                "solver__multi_class__multi_class_method": Categorical(
                    "solver__multi_class__multi_class_method",
                    ["allclass_domain", "loop", "splitable_domain"],
                    default="allclass_domain",
                ),
                "solver__multi_class__label_batch_size": Integer(
                    "solver__multi_class__label_batch_size",
                    (1, 128),
                    default=32,
                ),
                "solver__multi_class__skip_with_refined_bound": Categorical(
                    "solver__multi_class__skip_with_refined_bound",
                    [True, False],
                    default=True,
                ),
                "solver__mip__parallel_solvers": Categorical(
                    "solver__mip__parallel_solvers",
                    ["null"],
                    default="null",
                ),
                "solver__mip__refine_neuron_timeout": Integer(
                    "solver__mip__refine_neuron_timeout",
                    (1, 30),
                    default=15,
                ),
                "solver__mip__refine_neuron_time_percentage": Float(
                    "solver__mip__refine_neuron_time_percentage",
                    (0.0, 1.0),
                    default=0.8,
                ),
                "solver__mip__early_stop": Categorical(
                    "solver__mip__early_stop",
                    [True, False],
                    default=True,
                ),
                "solver__mip__adv_warmup": Categorical(
                    "solver__mip__adv_warmup",
                    [True, False],
                    default=True,
                ),
                "solver__mip__mip_solver": Constant(
                    "solver__mip__mip_solver",
                    "gurobi",
                ),
                # bab
                "bab__pruning_in_iteration": Categorical(
                    "bab__pruning_in_iteration",
                    [True, False],
                    default=True,
                ),
                "bab__pruning_in_iteration_ratio": Float(
                    "bab__pruning_in_iteration_ratio",
                    (0.0, 1.0),
                    default=0.2,
                ),
                "bab__sort_targets": Categorical(
                    "bab__sort_targets",
                    [True, False],
                    default=False,
                ),
                "bab__bached_domain_list": Categorical(
                    "bab__bached_domain_list",
                    [True, False],
                    default=True,
                ),
                "bab__cut__enabled": Categorical(
                    "bab__cut__enabled",
                    [True, False],
                    default=False,
                ),
                "bab__cut__bab_cut": Categorical(
                    "bab__cut__bab_cut",
                    [True, False],
                    default=False,
                ),
                "bab__cut__method": Constant(
                    "bab__cut__method",
                    "null",
                ),
                "bab__cut__lr": Float(
                    "bab__cut__lr",
                    (0.001, 0.2),
                    default=0.01,
                ),
                "bab__cut__lr_decay": Float(
                    "bab__cut__lr_decay",
                    (0.9, 1.0),
                    default=1.0,
                ),
                "bab__cut__iteration": Integer(
                    "bab__cut__iteration",
                    (10, 200),
                    default=100,
                ),
                "bab__cut__bab_iteration": Constant(
                    "bab__cut__bab_iteration",
                    -1,
                ),
                "bab__cut__lr_beta": Float(
                    "bab__cut__lr_beta",
                    (0.001, 0.2),
                    default=0.02,
                ),
                "bab__cut__number_cuts": Integer(
                    "bab__cut__number_cuts",
                    (1, 100),
                    default=50,
                ),
                "bab__cut__topk_cuts_in_filter": Integer(
                    "bab__cut__topk_cuts_in_filter",
                    (1, 200),
                    default=100,
                ),
                "bab__cut__batch_size_primal": Integer(
                    "bab__cut__batch_size_primal",
                    (1, 200),
                    default=100,
                ),
                "bab__cut__max_num": Integer(
                    "bab__cut__max_num",
                    (100_000_000, 10_000_000_000),
                    default=1_000_000_000,
                ),
                "bab__cut__patches_cut": Categorical(
                    "bab__cut__patches_cut",
                    [True, False],
                    default=False,
                ),
                "bab__cut__cplex_cuts": Categorical(
                    "bab__cut__cplex_cuts",
                    [True, False],
                    default=False,
                ),
                "bab__cut__cplex_cuts_wait": Float(
                    "bab__cut__cplex_cuts_wait",
                    (0, 2),
                    default=0,
                ),
                "bab__cut__cplex_cuts_revpickup": Categorical(
                    "bab__cut__cplex_cuts_revpickup",
                    [True, False],
                    default=True,
                ),
                "bab__cut__cut_reference_bounds": Categorical(
                    "bab__cut__cut_reference_bounds",
                    [True, False],
                    default=True,
                ),
                "bab__cut__fix_intermediate_bounds": Categorical(
                    "bab__cut__fix_intermediate_bounds",
                    [True, False],
                    default=False,
                ),
                "bab__branching__method": Categorical(
                    "bab__branching__method",
                    ["kfsb", "babsr", "fsb", "kfsb-intercept-only", "sb"],
                    default="kfsb",
                ),
                "bab__branching__candidates": Integer(
                    "bab__branching__candidates",
                    (1, 10),
                    default=3,
                ),
                "bab__branching__reduceop": Categorical(
                    "bab__branching__reduceop",
                    ["min", "max"],
                    default="min",
                ),
                "bab__branching__sb_coeff_thresh": Float(
                    "bab__branching__sb_coeff_thresh",
                    (0.000_01, 0.001),
                    default=0.001,
                ),
                "bab__branching__input_split__enable": Categorical(
                    "bab__branching__input_split__enable",
                    [True, False],
                    default=False,
                ),
                # TODO: Options for below
                "bab__branching__input_split__enhanced_bound_prop_method": Categorical(  # noqa: E501
                    "bab__branching__input_split__enhanced_bound_prop_method",
                    ["alpha-crown"],
                    default="alpha-crown",
                ),
                # TODO: Options for below
                "bab__branching__input_split__enhanced_branching_method": Categorical(  # noqa: E501
                    "bab__branching__input_split__enhanced_branching_method",
                    ["naive"],
                    default="naive",
                ),
                "bab__branching__input_split__enhanced_bound_patience": Float(
                    "bab__branching__input_split__enhanced_bound_patience",
                    (10_000_000.0, 1_000_000_000.0),
                    default=100_000_000.0,
                ),
                "bab__branching__input_split__attack_patience": Float(
                    "bab__branching__input_split__attack_patience",
                    (10_000_000.0, 1_000_000_000.0),
                    default=100_000_000.0,
                ),
                "bab__branching__input_split__adv_check": Integer(
                    "bab__branching__input_split__adv_check",
                    (0, 10),
                    default=-0,
                ),
                "bab__branching__input_split__sort_domain_interval": Integer(
                    "bab__branching__input_split__sort_domain_interval",
                    (-1, 10),
                    default=-1,
                ),
                # bab-branching-attack
                # attack
                "attack__pgd_order": Categorical(
                    "attack__pgd_order",
                    ["before", "after"],
                    default="before",
                ),
                "attack__pgd_steps": Integer(
                    "attack__pgd_steps",
                    (1, 200),
                    default=100,
                ),
                "attack__pgd_restarts": Integer(
                    "attack__pgd_restarts",
                    (1, 60),
                    default=30,
                ),
                "attack__pgd_early_stop": Categorical(
                    "attack__pgd_early_stop",
                    [True, False],
                    default=True,
                ),
                "attack__pgd_lr_decay": Float(
                    "attack__pgd_lr_decay",
                    (0.9, 1.0),
                    default=0.99,
                ),
                "attack__pgd_alpha": Categorical(
                    "attack__pgd_alpha",
                    ["auto"],
                    default="auto",
                ),
                "attack__pgd_loss_mode": Categorical(
                    "attack__pgd_loss_mode",
                    ["null"],
                    default="null",
                ),
                "attack__enable_mip_attack": Categorical(
                    "attack__enable_mip_attack",
                    [True, False],
                    default=False,
                ),
                "attack__attack_mode": Categorical(
                    "attack__attack_mode",
                    ["PGD", "GAMA"],
                    default="PGD",
                ),
                "attack__gama_lambda": Float(
                    "attack__gama_lambda",
                    (1.0, 20.0),
                    default=1.0,
                ),
                "attack__gama_decay": Float(
                    "attack__gama_decay",
                    (0.8, 1.0),
                    default=0.9,
                ),
                "attack__check_clean": Categorical(
                    "attack__check_clean",
                    [True, False],
                    default=False,
                ),
                "attack__input_split__pgd_steps": Integer(
                    "attack__input_split__pgd_steps",
                    (1, 200),
                    default=100,
                ),
                "attack__input_split__pgd_restarts": Integer(
                    "attack__input_split__pgd_restarts",
                    (1, 60),
                    default=30,
                ),
                "attack__input_split__pgd_alpha": Categorical(
                    "attack__input_split__pgd_alpha",
                    ["auto"],
                    default="auto",
                ),
                "attack__input_split_enhanced__pgd_steps": Integer(
                    "attack__input_split_enhanced__pgd_steps",
                    (1, 400),
                    default=100,
                ),
                "attack__input_split_enhanced__pgd_restarts": Integer(
                    "attack__input_split_enhanced__pgd_restarts",
                    (100000, 10000000),
                    default=5000000,
                ),
                "attack__input_split_enhanced__pgd_alpha": Categorical(
                    "attack__input_split_enhanced__pgd_alpha",
                    ["auto"],
                    default="auto",
                ),
                "attack__input_split_check_adv__pgd_steps": Integer(
                    "attack__input_split_check_adv__pgd_steps",
                    (1, 400),
                    default=100,
                ),
                "attack__input_split_check_adv__pgd_restarts": Integer(
                    "attack__input_split_check_adv__pgd_restarts",
                    (100000, 10000000),
                    default=5000000,
                ),
                "attack__input_split_check_adv__pgd_alpha": Categorical(
                    "attack__input_split_check_adv__pgd_alpha",
                    ["auto"],
                    default="auto",
                ),
            },
        ),
    }
)
