# -*- coding: utf-8 -*-

import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
cmd_handler = logging.StreamHandler(sys.stdout)
cmd_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
cmd_handler.setFormatter(formatter)
logger.addHandler(cmd_handler)
