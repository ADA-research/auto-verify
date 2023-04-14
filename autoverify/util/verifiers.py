"""_summary_."""
from autoverify.verifier import DummyVerifier, Nnenum


# TODO: Dont hardcore this
def get_all_complete_verifier_names() -> list[str]:
    """Return a list of all complete verifier names."""
    return [
        DummyVerifier.name,
        Nnenum.name,
    ]
