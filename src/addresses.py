# Constants and utility related to addresses

from typing import NamedTuple, List


# address of a worker, includes a ip address and a port number
class Address(NamedTuple):
    ip: str
    port: int


# the server address for interface
# if it is localhost, then it is for testing purpose.
INTERFACE_ADDRESS = Address("localhost", 5000)

# list of worker addresses
# if it is localhost, then it is for testing purpose.
WORKER_ADDRESSES: List[Address] = [
    Address("localhost", 69),
    Address("localhost", 420)
]