import logging

from config import DEBUG

LOGGING_LVL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=LOGGING_LVL)
logger = logging.getLogger(__name__)
