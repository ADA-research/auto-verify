"""_summary_."""
from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    Constant,
    Float,
    Integer,
)

MnBabConfigspace = ConfigurationSpace()
"""
ADD AFTER SAMPLE:
    - network_path
    - input_dim
    - benchmark_instances_path
    - use_gpu
    - bab_batch_sizes
    - random_seed
    - timeout
    - experiment_name
"""
# TODO: parameter_sharing params
MnBabConfigspace.add_hyperparameters(
    [
        Constant("eps", 0),
        Constant("test_data_path", ""),
        Constant("dtype", "float64"),
        Categorical(
            "outer_verifier__forward_dp_pass",
            [True, False],
            default=False,
        ),
        Categorical(
            "outer_verifier__initial_dp",
            [True, False],
            default=True,
        ),
        Categorical(
            "outer_verifier__input_domain_splitting",
            [True, False],
            default=False,
        ),
        Categorical(
            "outer_verifier__adversarial_attack",
            [True, False],
            default=False,
        ),
        Integer(
            "outer_verifier__adversarial_attack_restarts",
            (1, 10),
            default=5,
        ),
        Categorical(
            "outer_verifier__milp__solve_via_milp",
            [True, False],
            default=False,
        ),
        Integer(
            "outer_verifier__milp__refine_via_milp",
            (1, 5),
            default=2,
        ),
        Integer(
            "outer_verifier__milp__timeout_refine_total",
            (30, 400),
            default=200,
        ),
        Integer(
            "outer_verifier__milp__timeout_refine_neuron",
            (1, 10),
            default=5,
        ),
        Categorical(
            "outer_verifier__refine_intermediate_bounds",
            [True, False],
            default=False,
        ),
        Categorical(
            "outer_verifier__refine_intermediate_bounds_prima",
            [True, False],
            default=False,
        ),
        Categorical(
            "outer_verifier__simplify_onnx",
            [True, False],
            default=False,
        ),
        Integer(
            "domain_splitting__initial_splits",
            (1, 6),
            default=3,
        ),
        Integer(
            "domain_splitting__max_depth",
            (5, 15),
            default=10,
        ),
        Categorical(
            "domain_splitting__domain",
            ["zono", "box", "hbox", "DPF", "none", "dp"],
            default="dp",
        ),
        Integer(
            "domain_splitting__batch_sizd",
            (25, 300),
            default=100,
        ),
        Integer(
            "domain_splitting__split_factor",
            (1, 6),
            default=3,
        ),
        Constant(  # TODO:
            "domain_splitting__initial_split_dims",
            0,  # [0],
        ),
        Integer(
            "max_num_queries",
            (500, 1500),
            default=500,
        ),
        Categorical(
            "optimize_alpha",
            [True, False],
            default=True,
        ),
        Float(
            "alpha_lr",
            (0.01, 0.2),
            default=0.1,
        ),
        Categorical(
            "relu_alpha_init_method",
            ["minimum_area", "one_half"],
            default="minimum_area",
        ),
        Integer(
            "alpha_opt_iterations",
            (1, 40),
            default=20,
        ),
        Categorical(
            "optimize_prima",
            [True, False],
            default=True,
        ),
        Float(
            "prima_lr",
            (0.001, 0.1),
            default=0.01,
        ),
        Integer(
            "prima_opt_iterations",
            (1, 40),
            default=20,
        ),
        Integer(
            "prima_hyperparameters__sparse_n",
            (25, 75),
            default=50,
        ),
        Integer(
            "prima_hyperparameters__K",
            (1, 6),
            default=3,
        ),
        Integer(
            "prima_hyperparameters__s",
            (1, 4),
            default=1,
        ),
        Integer(  # TODO: This should respect any CPU core constraints we set
            "prima_hyperparameters__num_proc_to_compute_constraints",
            (1, 2),
            default=2,
        ),
        Integer(
            "prima_hyperparameters__max_number_of_parallel_input_constraint_queries",  # noqa: E501
            (1000, 20000),
            default=10000,
        ),
        Integer(
            "prima_hyperparameters__max_unstable_nodes_considered_per_layer",
            (100, 2000),
            default=1000,
        ),
        Float(
            "prima_hyperparameters__min_rely_transformer_area_to_be_considered",
            (0.001, 0.1),
            default=0.01,
        ),
        Float(
            "prima_hyperparameters__fraction_of_constraints_to_keep",
            (0.9, 1.0),
            default=1.0,
        ),
        Categorical(
            "prima_hyperparameters__random_prima_groups",
            ["none", "only", "augment"],
            default="none",
        ),
        Float(
            "prima_hyperparameters__prima_sparsity_factor",
            (0.9, 1.0),
            default=1.0,
        ),
        Float(
            "peak_lr_scaling_factor",
            (1.0, 3.0),
            default=2.0,
        ),
        Float(
            "final_lr_div_factor",
            (5.0, 15.0),
            default=10.0,
        ),
        Float(
            "beta_lr",
            (0.25, 0.75),
            default=0.5,
        ),
        Categorical(
            "branching__method",
            ["babsr", "active_constraint_score", "filtered_smart_branching"],
            default="babsr",
        ),
        Categorical(
            "branching__use_prima_contributions",
            [True, False],
            default=False,
        ),
        Categorical(
            "branching__use_optimized_slopes",
            [True, False],
            default=False,
        ),
        Categorical(
            "branching__use_beta_contributions",
            [True, False],
            default=False,
        ),
        Categorical(
            "branching__propagation_effect_mode",
            ["bias", "none", "intermediate_concretization"],
            default="bias",
        ),
        Categorical(
            "branching__use_indirect_effect",
            [True, False],
            default=False,
        ),
        Categorical(
            "branching__reduce_op",
            ["geo_mean", "min", "max"],
            default="geo_mean",
        ),
        Categorical(
            "branching__use_abs",
            [True, False],
            default=True,
        ),
        Categorical(
            "branching__use_cost_adjusted_scores",
            [True, False],
            default=False,
        ),
        Categorical(
            "run_BaB",
            [True, False],
            default=True,
        ),
        Categorical(
            "box_pass",
            [True, False],
            default=True,
        ),
        Categorical(
            "recompute_intermediate_bounds_after_branching",
            [True, False],
            default=False,
        ),
        Categorical(
            "intermediate_bounds_method",
            # TODO: There is an ordering here (none < dp < alpha < prima),
            # that may cause issues
            ["none", "dp", "alpha", "prima"],
            default="prima",
        ),
        Categorical(
            "use_dependence_sets",
            [True, False],
            default=False,
        ),
        Categorical(
            "use_early_termination",
            [True, False],
            default=True,
        ),
        Constant("comet_api_key", "-"),
        Constant("comet_project_name", "-"),
        Constant("comet_workspace", "-"),
    ]
)
