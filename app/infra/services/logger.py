import sys

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", serialize=True, backtrace=True, diagnose=True)
