from typing import Type

from ConfigSpace import Categorical, ConfigurationSpace

from autoverify.verifier.verifier import CompleteVerifier


def make_select_verifier_configspace(
    verifiers: list[Type[CompleteVerifier]],
    *,
    default: str | None = None,
) -> ConfigurationSpace:
    """_summary_."""
    verifier_names = [verifier().name for verifier in verifiers]

    return ConfigurationSpace(
        {"verifier": Categorical("verifier", verifier_names, default=default)}
    )
