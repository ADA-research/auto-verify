from pathlib import Path

from result import Err, Ok

from autoverify.portfolio.run.sequential_runner import run_sequential_portfolio
from autoverify.util.env import get_file_path
from autoverify.util.instances import (
    VerificationInstance,
    read_vnncomp_instances,
)
from autoverify.verifier.complete import AbCrown


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
        features[inst] = [size]

    return features


if __name__ == "__main__":
    mnist_instances = read_vnncomp_instances("mnist_fc")
    mnist_instances = filter_to_small(mnist_instances)
    file_path = get_file_path(Path(__file__))

    ab = AbCrown()

    for instance in mnist_instances:
        cfg = ab.sample_configuration()
        print("+" * 80)
        print(cfg)
        print("+" * 80)

        result = ab.verify_property(
            instance.network, instance.property, config=cfg
        )

        if isinstance(result, Ok):
            print("Verification finished succesfully.")
            print(f"Result: {result.value.result}")
        elif isinstance(result, Err):
            print("Exception during verification.")
            print(result.unwrap_err())
        print("=" * 80)
