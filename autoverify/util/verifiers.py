"""_summary_."""
from autoverify.verifier import AbCrown, DummyVerifier, MnBab, Nnenum


# TODO: Dont hardcode this
def get_all_complete_verifier_names() -> list[str]:
    """Return a list of all complete verifier names."""
    return [
        DummyVerifier.name,
        Nnenum.name,
        AbCrown.name,
        MnBab.name,
    ]
