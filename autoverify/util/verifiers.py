"""Hardcoded verifier utility."""
from ConfigSpace import ConfigurationSpace

from autoverify.verifier import AbCrown, MnBab, Nnenum, OvalBab, Verinet
from autoverify.verifier.verifier import Verifier


# HACK: Should be an attribute of the verifier
# Ideally something that specifies wether it can or
# always uses the GPU. This is mainly needed for
# resource allocation in portfolios.
def uses_gpu(verifier: str) -> bool:
    """Returns if this verifier uses the GPU."""
    verifier = verifier.lower()

    if verifier == "abcrown":
        return True
    elif verifier == "nnenum":
        return False
    elif verifier == "verinet":
        return True
    elif verifier == "ovalbab":
        return True
    elif verifier == "mnbab":
        return True

    raise ValueError(f"Invalid verifier name: {verifier}")


# TODO: Dont hardcode this
def get_all_complete_verifier_names() -> list[str]:
    """Return a list of all complete verifier names."""
    return [
        Nnenum.name,
        AbCrown.name,
        OvalBab.name,
        Verinet.name,
        # MnBab.name,
    ]


def get_verifier_configspace(verifier: str) -> ConfigurationSpace:
    """Get the Configuration Space of a verifier by name."""
    return verifier_from_name(verifier)().config_space


# TODO: Dont hardcode this
def verifier_from_name(name: str) -> type[Verifier]:
    """Return the class type from the verifier name."""
    if name == "abcrown":
        return AbCrown
    elif name == "nnenum":
        return Nnenum
    elif name == "mnbab":
        return MnBab
    elif name == "ovalbab":
        return OvalBab
    elif name == "verinet":
        return Verinet

    raise ValueError(f"Invalid verifier name: {name}")
