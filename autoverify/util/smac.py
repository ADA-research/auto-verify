"""SMAC util."""


from autoverify.util.instances import VerificationInstance


def index_features(
    instances: list[str] | list[VerificationInstance],
) -> dict[str, list[float]]:
    """Use indices as simple instance features."""
    features = {}

    for i, inst in enumerate(instances):
        k = inst

        if isinstance(inst, VerificationInstance):
            k = inst.as_smac_instance()

        features[k] = [float(i)]

    return features
