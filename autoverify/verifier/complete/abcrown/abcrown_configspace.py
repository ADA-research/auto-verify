"""_summary_."""
from ConfigSpace import Categorical, ConfigurationSpace, Float, Integer

from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)

AbCrownConfigspace = VerifierConfigurationSpace(
    {
        ConfigurationLevel.SOLVER: ConfigurationSpace(
            space={"uniform_integer_solver": (1, 10)}
        ),
        ConfigurationLevel.VERIFIER: ConfigurationSpace(
            name="abcrown_verifier",
            seed=42,
            space={
                "device": ["cuda"],  # cuda or cpu
            },
        ),
    }
)
