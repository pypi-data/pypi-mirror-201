import logging
import os.path

# this import statement is here for context.py in tests folder
from .visualtest import VisualTest

__version__ = '1.2.0'

logPath = 'logs'
if not os.path.exists(logPath):
    os.makedirs(logPath)

# By generating a new logger as 'vt' we don't affect global logging from other packages
# Each logger created in our package should be a child by prefacing with 'vt.childname'
logger = logging.getLogger('vt')
formatter = logging.Formatter('%(asctime)s [%(name)s][%(levelname)s] %(message)s')

fileHandler = logging.FileHandler(os.path.join(logPath,'info.log'), mode='w')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

if "LOGGER_LEVEL" in os.environ:
    LOGGER_LEVEL = os.environ["PROJECT_TOKEN"]
    print(f'LOGGER_LEVEL: {LOGGER_LEVEL}')
    logger.setLevel(level=LOGGER_LEVEL)
else:
    logger.setLevel(level='INFO')

# decided to only add console logging from instantiation of VisualTesting class
# - see visualtest.py
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(formatter)
# logger.addHandler(consoleHandler)
# logger.setLevel(logging.WARNING)

