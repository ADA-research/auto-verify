"""_summary_."""
import time
from pathlib import Path
from typing import Callable, Type

from ConfigSpace import Configuration

from autoverify.verifier.verifier import CompleteVerifier

# target_function(config, instance, seed) -> cost
SmacTargetFunction = Callable[[Configuration, str, int], float]


def make_verifier_target_function(
    verifier: Type[CompleteVerifier],
    *,
    timeout_penalty: int = 10,
) -> SmacTargetFunction:
    """Return a new target_function that uses the specified verifier.

    Args:
        verifier: The verifier class to use in the target function.
        timeout_penalty: The multiplier used for instances that have
            timed out, `cost *= timeout_penalty`.

    Returns:
        SmacTargetFunction: The target function that can be used inside
            a SMAC facade.
    """

    def target_function(
        config: Configuration, instance: str, seed: int = 1
    ) -> float:
        """_summary_."""
        seed += 1  # silence warning, cant rename the param to _ or smac errors

        verifier_instance = verifier()
        network, property = instance.split(",")

        before_t = time.process_time()
        result = verifier_instance.verify_property(
            Path(network), Path(property), config=config
        )
        took_t = time.process_time() - before_t

        # If the result is an err, we raise an exception. SMAC automatically
        # sets the cost to infinite if an exception is raised in the target_func
        verification_result = result.unwrap_or_raise(Exception)

        if verification_result.result == "TIMEOUT":
            took_t *= timeout_penalty

        return took_t

    return target_function
