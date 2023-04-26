"""Module-wide loggers."""
import logging

root_logname = "[auto-verify::{}]"

logging.basicConfig(level=logging.NOTSET)

install_logger = logging.getLogger(root_logname.format("install"))
install_logger.setLevel(logging.INFO)
