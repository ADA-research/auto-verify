from copy import deepcopy

from ConfigSpace import ConfigurationSpace

from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)


# TODO this function is not verbose enough, cant tell which vcs we are
# actually getting here. Needs a different pattern (also: return a copy of the
# vcs)
def get_configspace() -> VerifierConfigurationSpace:
    return VerifierConfigurationSpace(
        {
            ConfigurationLevel.SOLVER: ConfigurationSpace(
                space={"uniform_integer_solver": (1, 10)}
            ),
            ConfigurationLevel.VERIFIER: ConfigurationSpace(
                space={"uniform_integer_verifier": (1, 10)}
            ),
        }
    )
