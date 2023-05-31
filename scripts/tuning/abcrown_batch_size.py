import logging

from result import Err, Ok

from autoverify.util.instances import (
    filter_verification_instances,
    read_vnncomp_instances,
)
from autoverify.util.vnncomp_filters import mnist_large_filter
from autoverify.verifier import AbCrown

logger = logging.getLogger(__name__)

mnist_fc = read_vnncomp_instances("mnist_fc")
mnist_fc = filter_verification_instances(mnist_fc, mnist_large_filter)

if __name__ == "__main__":
    ab = AbCrown()

    for inst in mnist_fc:
        logger.info(f"{inst.network.name} {inst.property.name} {inst.timeout}")

        res = ab.verify_property(
            inst.network, inst.property, timeout=inst.timeout
        )

        if isinstance(res, Ok):
            logger.info("Verification went ok.")
            logger.info(f"verification result was: {res.ok().result}")
        elif isinstance(res, Err):
            logger.info("Verification errored.")
            logger.info(f"Err=\n{res.err()}")
