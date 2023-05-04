"""_summary_."""
from ConfigSpace import ConfigurationSpace

from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)

MnBabConfigspace = VerifierConfigurationSpace(
    {
        ConfigurationLevel.solver: ConfigurationSpace(
            space={"uniform_integer_solver": (1, 10)}
        ),
        ConfigurationLevel.verifier: ConfigurationSpace(
            space={"uniform_integer_verifier": (1, 10)}
        ),
    }
)
