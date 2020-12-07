import logging
from typing import List

from src.types import Address

# the logging setting for worker interface communication
# other setting can be set in logging_util
LOGGING_LEVEL = logging.DEBUG
LOGGING_FILE = None

# list of worker addresses
# if it is localhost, then it is for testing purpose.
WORKER_ADDRESSES: List[Address] = [
    Address("127.0.0.1", 65000)
]


