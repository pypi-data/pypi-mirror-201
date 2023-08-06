"""Tests for the logging module"""
from dkist_service_configuration import logger


def test_log_levels():
    logger.trace("trace")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
