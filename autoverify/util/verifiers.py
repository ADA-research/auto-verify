from autoverify.verifier import DummyVerifier


# TODO: Dont hardcore this somehow
def get_all_complete_verifier_names() -> list[str]:
    """Return a list of all complete verifier names."""
    return [
        DummyVerifier.name,
    ]
