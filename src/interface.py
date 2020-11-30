# the code for the interface server
# which will display the webpage to upload file
# and it will communicate with the server to assign file.
import socket
import random
from typing import Optional, NamedTuple, Dict, Set, List, Tuple

from .socket_util import receive_msg_from, send_msg_to, send_file_to
from .shared import Address, WORKER_ADDRESSES, \
    gen_message, parse_worker_task_num_msg, \
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


def image_recognition_with_worker(worker_address: Address,
                                  task_file_name: str) -> IRResult:
    """let a specific worker finish a image recognition task

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


def image_recognition(task_file_name: str) -> IRResult:
    """Let the desirable worker finish the given image recognition task

    :param task_file_name: the input file to recognize
    :return: the image recognition result
    """

    # get all the task num of all the workers
    workers_with_task_nums = [(worker_addr, get_worker_task_num(worker_addr))
                              for worker_addr in WORKER_ADDRESSES]

    # filter out those who did not successfully return the result
    success_worker_task_nums: List[Tuple[Address, int]] = [
        (worker_addr, worker_task_num)
        for (worker_addr, worker_task_num) in workers_with_task_nums
        if worker_task_num is not None
    ]

    # get the worker with the least number of tasks (least_task_worker)
    worker_with_least_task_num = min(
        success_worker_task_nums,
        # only compare the task nums
        key=lambda worker_with_task_num: worker_with_task_num[1]
    )
    (least_task_worker, _) = worker_with_least_task_num

    # do the image recognition with the least task worker
    return image_recognition_with_worker(least_task_worker, task_file_name)
