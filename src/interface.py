# the code for the interface server
# which will display the webpage to upload file
# and it will communicate with the server to assign file.
import socket
import random
from typing import Optional, NamedTuple, Dict, Set

from .socket_util import receive_msg_from, send_msg_to, send_file_to
from .shared import Address, \
    gen_message, parse_worker_task_num_msg,  \
    NewTaskToWorkerMsg, parse_ir_result_msg, IRResult


def get_worker_task_num(worker_address: Address) -> Optional[int]:
    """Get a task num from a worker

    If the worker no longer accepts task, return None
    :param worker_address: the address of the worker
    :return: If the worker is accepting task,
        return the current task that the worker has,
        else None
    """
    # generate the message to pin the worker
    new_task_msg = NewTaskToWorkerMsg()

    # TODO: timeout?
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        # connecting with the worker
        conn.connect((worker_address.ip, worker_address.port))
        print("connected to worker", (worker_address.ip, worker_address.port))

        # send the message and parse the result
        send_msg_to(conn, gen_message(new_task_msg))
        task_num_msg_str = receive_msg_from(conn)
        task_num_msg = parse_worker_task_num_msg(task_num_msg_str)

        # return the result
        # if the worker is no longer accepting task, then return None
        if task_num_msg.accepting_task:
            return task_num_msg.task_num
        else:
            return None


def assign_task_to(worker_address: Address, task_file_name: str) -> IRResult:
    """Assign a specific task to a given worker

    :param worker_address: the address of the worker to assign to
    :param task_file_name: the file name of the task
    """
    # TODO: timeout?
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        # connecting with the worker
        conn.connect((worker_address.ip, worker_address.port))
        print("connected to worker", (worker_address.ip, worker_address.port))

        # send the image for the task
        send_file_to(conn, task_file_name)

        # receive the result
        ir_result_str = receive_msg_from(conn)
        # make sure the respond is valid
        ir_result_msg = parse_ir_result_msg(ir_result_str)

        return ir_result_msg.result


