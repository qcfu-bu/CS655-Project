# General Utility for socket uses
import socket
import struct

from src.logging_util import Logger

K = 1024

TIMEOUT_TIME = 60  # seconds

DATA_CAP = 1 * K  # data to send in a single packet
ENCODING = 'utf-8'  # use utf-8 for text encoding

MSG_ENDING_CHAR = b'\n'  # this char signifies the ending of a message

LOGGER = Logger(logging_from="SOCKET")


def receive_msg_from(connection: socket.socket) -> str:
    """receiving data from the connection

    :param connection: a accepted socket connection
    :return: raw message that ends with \n
    """
    # setting the timeout time
    connection.settimeout(TIMEOUT_TIME)
    LOGGER.debug(f"Setting timeout time to {TIMEOUT_TIME} seconds")

    LOGGER.info(f"receiving message from connection")

    # receive a packet first
    cur_recv: bytes = connection.recv(DATA_CAP)
    LOGGER.debug(f"received part of the message: {cur_recv}")
    # if it is empty, then we exit,
    # since empty packet indicates that the other side has disconnected
    if cur_recv == b"":
        raise ConnectionError("Other side has disconnected.")

    # receives the rest of the package
    total_recv = cur_recv
    while not cur_recv.endswith(MSG_ENDING_CHAR):
        cur_recv: bytes = connection.recv(DATA_CAP)
        LOGGER.debug(f"received part of the message: {cur_recv}")
        total_recv = total_recv + cur_recv

    LOGGER.info(f"total message Received: {repr(total_recv.decode(ENCODING))}")

    return total_recv.decode(ENCODING)


def send_msg_to(connection: socket.socket, msg: str) -> None:
    """Send a generic message to the server

    :param connection: an accepted connection
    :param msg: the message to send
    """
    # setting the timeout time
    connection.settimeout(TIMEOUT_TIME)
    LOGGER.debug(f"Setting timeout time to {TIMEOUT_TIME} seconds")

    LOGGER.info(f"sending message: {repr(msg)}")
    connection.sendall(msg.encode(ENCODING) + MSG_ENDING_CHAR)


def send_file_to(connection: socket.socket, send_file_name: str) -> None:
    """send a file through the connection

    :param connection: the connection to send to
    :param send_file_name: the name of the file to send
    """
    # setting the timeout time
    connection.settimeout(TIMEOUT_TIME)
    LOGGER.debug(f"Setting timeout time to {TIMEOUT_TIME} seconds")

    LOGGER.info(f"Starting to send file {send_file_name}")

    with open(send_file_name, 'rb') as f:
        file_content = f.read()
    file_size = len(file_content)

    LOGGER.debug(f"total file content size: {file_size}")
    connection.sendall(struct.pack(">L", file_size) + file_content)

    LOGGER.info(f"finish sending file {send_file_name}")


def receive_file_from(connection: socket.socket, save_file_name: str) -> None:
    """Receives a file from the connection

    :param connection: the connection to receive file from
    :param save_file_name: the file name to save
    """
    # setting the timeout time
    connection.settimeout(TIMEOUT_TIME)

    LOGGER.debug(f"Setting timeout time to {TIMEOUT_TIME} seconds")
    LOGGER.info(f"starting to receive file")

    data_recv = b""
    payload_size = struct.calcsize(">L")
    LOGGER.info(f"Payload_size: {payload_size}")

    while len(data_recv) < payload_size:
        data_recv += connection.recv(DATA_CAP)

    packed_msg_size = data_recv[:payload_size]
    data_recv = data_recv[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    LOGGER.info(f"msg_size: {msg_size}")

    while len(data_recv) < msg_size:
        data_recv += connection.recv(DATA_CAP)

    data_recv = data_recv[:msg_size]

    with open(save_file_name, 'wb') as f:
        f.write(data_recv)

    LOGGER.info(f"file received and saved to {save_file_name}")
