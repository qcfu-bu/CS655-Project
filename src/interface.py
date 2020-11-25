# the code for the interface server
# which will display the webpage to upload file
# and it will communicate with the server to assign file.
import socket
from typing import Optional

from addresses import Address
from socket_util import receive_data_from, send_message
from worker_interface_message import gen_message, parse_worker_task_num_msg, \
    WorkerTaskNumMsg, NewTaskToWorkerMsg


def get_worker_task_num(worker_address: Address) -> Optional[int]:

    # generate the message to pin the worker
    new_task_msg = NewTaskToWorkerMsg()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        # connecting with the worker
        conn.connect((worker_address.ip, worker_address.port))
        print("connected to host", (worker_address.ip, worker_address.port))

        # send the message and parse the result
        task_num_msg_str = send_message(conn, gen_message(new_task_msg))
        task_num_msg = parse_worker_task_num_msg(task_num_msg_str)

        # return the result
        # if the worker is no longer accepting task, then return None
        if task_num_msg.accepting_task:
            return task_num_msg.task_num
        else:
            return None










