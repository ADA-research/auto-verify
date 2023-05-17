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
    features = {}

    for inst in mnist_instances:
        size = inst.network.name.split(".")[0][-1]
        features[inst] = [float(size)]

    return features
