# the code for the interface server
# which will display the webpage to upload file
# and it will communicate with the server to assign file.
import socket
from typing import Optional, List, Tuple

from src.logging_util import Logger
from src.socket_util import receive_msg_from, send_msg_to, send_file_to
from src.types import Address, \
    gen_message, parse_ir_result_msg, IRResult, TaskAssignMessage, \
    parse_success_respond_msg


LOGGER = Logger(logging_from="INTERFACE")


def image_recognition_with_worker(worker_address: Address,
                                  task_file_name: str) -> IRResult:
    """let a specific worker finish a image recognition task

    :param worker_address: the address of the worker to assign to
    :param task_file_name: the file name of the task
    """
    LOGGER.info(f"attempting to communicate with worker:"
                f"{worker_address.ip}: {worker_address.port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        # connecting with the worker
        conn.connect((worker_address.ip, worker_address.port))
        LOGGER.info(f"connected to worker: "
                    f"{worker_address.ip}: {worker_address.port}")

        LOGGER.info(f"sending task assignment message")
        # send the task assignment message
        send_msg_to(conn, gen_message(
            TaskAssignMessage(file_name=task_file_name)
        ))
        success_msg_str = receive_msg_from(conn)
        # validate the message
        _ = parse_success_respond_msg(success_msg_str)

        LOGGER.info("sending the image file")
        # send the image for the task
        send_file_to(conn, task_file_name)

        LOGGER.info("waiting for the IR result")
        # receive the result
        ir_result_str = receive_msg_from(conn)
        # make sure the respond is valid
        ir_result_msg = parse_ir_result_msg(ir_result_str)

    LOGGER.info(f"IR result obtained: {ir_result_msg.result}")
    return ir_result_msg.result

