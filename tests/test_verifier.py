from ConfigSpace import ConfigurationSpace

from autoverify.verifier.verification_result import CompleteVerificationResult
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verifier.verifier_configuration_space import (
    ConfigurationLevel,
    VerifierConfigurationSpace,
)

MyVcs = VerifierConfigurationSpace(
    {
        ConfigurationLevel.SOLVER: ConfigurationSpace(
            space={"uniform_integer_solver": (1, 10)}
        ),
        ConfigurationLevel.VERIFIER: ConfigurationSpace(
            space={"uniform_integer_verifier": (1, 10)}
        ),
    }
)


class MyVerifier(CompleteVerifier):
    @property
    def name(self):
        return "MyVerifier"

    @property
    def verifier_configspace(self) -> VerifierConfigurationSpace:
        return MyVcs

    def verify_property(self, property, network) -> CompleteVerificationResult:
        return super().verify_property(property, network)

    def sample_configuration(
        self, config_levels: set[ConfigurationLevel], size: int
    ):
        return super().sample_configuration(config_levels, size)


a = MyVerifier()
