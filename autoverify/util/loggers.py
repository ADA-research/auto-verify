"""Module-wide loggers."""
import logging

root_logname = "[auto-verify::{}]"

logging.basicConfig(level=logging.NOTSET)

install_logger = logging.getLogger(root_logname.format("install"))
install_logger.setLevel(logging.INFO)

verification_logger = logging.getLogger(root_logname.format("verify"))
verification_logger.setLevel(logging.DEBUG)

hydra_logger = logging.getLogger(root_logname.format("hydra"))
hydra_logger.setLevel(logging.DEBUG)

experiment_logger = logging.getLogger(root_logname.format("experiment"))
experiment_logger.setLevel(logging.INFO)
