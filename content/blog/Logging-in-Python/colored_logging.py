#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys

logger = logging.getLogger(__name__)


class Color:
    reset = '\x1b[0m'
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'


# logic from https://stackoverflow.com/a/75339761
class ColorLevelFormatter(logging.Formatter):

    _color_levelname = {
        'DEBUG': f"{Color.grey}DEBUG{Color.reset}",
        'INFO': f"{Color.blue}INFO{Color.reset}",
        'WARNING': f"{Color.yellow}WARNING{Color.reset}",
        'ERROR': f"{Color.red}ERROR{Color.reset}",
        'CRITICAL': f"{Color.bold_red}CRITICAL{Color.reset}",
    }

    def __init__(
            self,
            fmt: str = "%(levelname)s %(filename)s:%(lineno)s : %(message)s",
            *args,
            **kwargs,
    ):
        super().__init__(fmt, *args, **kwargs)

    def format(self, record):
        record.levelname = self._color_levelname[record.levelname]
        return super().format(record)


root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(ColorLevelFormatter())
root_logger.addHandler(stdout_handler)

logger.debug("Debugging information")
logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical issue")
