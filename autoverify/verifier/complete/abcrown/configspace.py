"""ab-crown configuration space."""

from ConfigSpace import (
    Categorical,
    ConfigurationSpace,
    Constant,
    EqualsCondition,
    Float,
    ForbiddenAndConjunction,
    ForbiddenEqualsClause,
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
        ########################################################################
        # BAB
        ########################################################################
        Categorical(
            "bab__cut__enabled",
            [True, False],
            default=False,
        ),
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
            "bab__attack__enabled",
            [True, False],
            default=False,
        ),
        ########################################################################
        # ATTACK
        ########################################################################
        Categorical(
            "attack__pgd_order",
            ["before", "middle", "after", "skip"],
            default="before",
        ),
        Categorical(
            "attack__attack_mode",
            ["diversed_PGD", "diversed_GAMA_PGD", "PGD", "boundary"],
            default="PGD",
        ),
    ]
)

AbCrownConfigspace.add_conditions(
    [
        EqualsCondition(
            AbCrownConfigspace[
                "bab__branching__input_split__enhanced_bound_prop_method"
            ],
            AbCrownConfigspace["bab__branching__input_split__enable"],
            True,
        ),
        NotEqualsCondition(
            AbCrownConfigspace["attack__attack_mode"],
            AbCrownConfigspace["attack__pgd_order"],
            "skip",
        ),
        EqualsCondition(
            AbCrownConfigspace["bab__cut__enabled"],
            AbCrownConfigspace["general__enable_incomplete_verification"],
            True,
        ),
    ]
)
AbCrownConfigspace.add_forbidden_clauses(
    [
        ForbiddenAndConjunction(
            ForbiddenEqualsClause(
                AbCrownConfigspace["bab__attack__enabled"], True
            ),
            ForbiddenEqualsClause(
                AbCrownConfigspace["general__enable_incomplete_verification"],
                False,
            ),
        ),
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
