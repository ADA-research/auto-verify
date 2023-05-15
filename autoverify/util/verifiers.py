"""_summary_."""
from typing import Type

from autoverify.verifier import AbCrown, DummyVerifier, MnBab, Nnenum, OvalBab
from autoverify.verifier.verifier import Verifier


# TODO: Dont hardcode this
def get_all_complete_verifier_names() -> list[str]:
    """Return a list of all complete verifier names."""
    return [
        DummyVerifier.name,
        Nnenum.name,
        AbCrown.name,
        MnBab.name,
        OvalBab.name,
    ]


# TODO: Dont hardcode this
def verifier_from_name(name: str) -> Type[Verifier] | None:
    """Return the class type from the verifier name."""
    if name == "abcrown":
        return AbCrown
    elif name == "nnenum":
        return Nnenum
    elif name == "mnbab":
        return MnBab
    elif name == "ovalbab":
        return OvalBab

    return None
