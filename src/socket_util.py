# General Utility for socket uses
import socket

K = 1024

DATA_CAP = 1 * K  # data to send in a single packet
ENCODING = 'utf-8'  # use utf-8 for text encoding

MSG_ENDING_CHAR = b'\n'  # this char signifies the ending of a message


def receive_data_from(connection: socket.socket) -> bytes:
    """receiving data from the connection

    :param connection: a accepted socket connection
    :return: raw message that ends with \n
    """
    total_recv = b""
    while True:
        cur_recv: bytes = connection.recv(DATA_CAP)
        if cur_recv.endswith(MSG_ENDING_CHAR):
            return total_recv + cur_recv
        else:
            total_recv = total_recv + cur_recv


def send_message(connection: socket.socket, msg: str) -> str:
    """Send a generic message to the server

    :param connection: an accepted connection
    :param msg: the message to send
    :return: the raw data received from server
    """
    connection.sendall(msg.encode(ENCODING) + MSG_ENDING_CHAR)
    data_recv = receive_data_from(connection)

    return data_recv.decode(ENCODING)
