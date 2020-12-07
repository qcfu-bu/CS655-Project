# General Utility for socket uses
import socket

from src.logging_util import Logger

K = 1024

TIMEOUT_TIME = 10  # seconds

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
    LOGGER.debug(f"Setting timeout time to {TIMEOUT_TIME}")

    LOGGER.info(f"receiving message from connection")
    total_recv = b""
    while True:
        cur_recv: bytes = connection.recv(DATA_CAP)
        LOGGER.debug(f"received part of the message: {cur_recv}")
        if cur_recv.endswith(MSG_ENDING_CHAR):
            total_recv = total_recv + cur_recv
            break
        else:
            total_recv = total_recv + cur_recv

    LOGGER.info(f"total message Received: {total_recv.decode(ENCODING)}")

    return total_recv.decode(ENCODING)


def send_msg_to(connection: socket.socket, msg: str) -> None:
    """Send a generic message to the server

    :param connection: an accepted connection
    :param msg: the message to send
    """
    # setting the timeout time
    connection.settimeout(TIMEOUT_TIME)
    LOGGER.debug(f"Setting timeout time to {TIMEOUT_TIME}")

    connection.sendall(msg.encode(ENCODING) + MSG_ENDING_CHAR)


def send_file_to(connection: socket.socket, send_file_name: str) -> None:
    """send a file through the connection

    :param connection: the connection to send to
    :param send_file_name: the name of the file to send
    """
    # setting the timeout time
    connection.settimeout(TIMEOUT_TIME)
    LOGGER.debug(f"Setting timeout time to {TIMEOUT_TIME}")

    LOGGER.info(f"Starting to send file {send_file_name}")

    with open(send_file_name, 'rb') as f:
        file_content = f.read()
        LOGGER.debug(f"total file content:\n{file_content}")
        connection.sendall(file_content)

    LOGGER.info(f"finish sending file {send_file_name}")


def receive_file_from(connection: socket.socket, save_file_name: str) -> None:
    """Receives a file from the connection

    :param connection: the connection to receive file from
    :param save_file_name: the file name to save
    """
    # setting the timeout time
    connection.settimeout(TIMEOUT_TIME)
    LOGGER.debug(f"Setting timeout time to {TIMEOUT_TIME}")

    LOGGER.info(f"starting to receive file")

    with open(save_file_name, 'wb') as f:

        # keeps receiving and write to file until there is nothing else
        # to receive.
        while True:
            data_recv = connection.recv(DATA_CAP)
            LOGGER.debug(f"received part of the message: {data_recv}")

            if len(data_recv) < DATA_CAP:
                break

            # write the currently received data to file
            f.write(data_recv)

    LOGGER.info(f"file recieved and saved to {save_file_name}")
