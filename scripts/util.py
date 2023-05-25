from autoverify.util.instances import VerificationInstance


def filter_to_small(
    mnist_instances: list[VerificationInstance],
) -> list[VerificationInstance]:
    small_instances = []

    for inst in mnist_instances:
        size = inst.network.name.split(".")[0][-1]

        if size == "2":
            small_instances.append(inst)

    return small_instances


def mnist_features(
    mnist_instances: list[VerificationInstance],
) -> dict[str, list[float]]:
    """Just using the 2,4,6 names in the network name as features for now."""
    features = {}

    for inst in mnist_instances:
        size = inst.network.name.split(".")[0][-1]
        features[inst.as_smac_instance()] = [float(size)]

    return features
