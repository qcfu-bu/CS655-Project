import socket
import threading
import uuid

from .socket_util import receive_file_from, send_msg_to, receive_msg_from

from .shared import IRResult, Address, gen_message, IRResultMsg, parse_task_assign_msg, SuccessRespondMsg

# the address of current worker
# if it is localhost then it is for testing
WORKER_ADDRESS = Address("localhost", 96)


def image_recognition(file_name: str) -> IRResult:
    """Perform the image recognition on the given file

    :param file_name: the name of the file to recognize
    """
    # TODO: sample output
    return {"dog": 1.0}


def run_ir_protocol(conn: socket.socket) -> None:
    """perform the image recognition protocol with the manager

    :param conn: the connection to the manager
    """
    with conn:
        print("connected, executing IR"),

        # receive information about this task assignment
        task_assign_msg_str = receive_msg_from(conn)
        task_assign_msg = parse_task_assign_msg(task_assign_msg_str)
        # get the file name for the task file
        file_name = task_assign_msg.file_name

        # indicate successfully get the file name
        send_msg_to(conn, gen_message(SuccessRespondMsg()))

        # generate a unique file name to save the file
        receive_file_from(conn, file_name)

        # do image recognition
        ir_result = image_recognition(file_name)

        # send the result
        send_msg_to(conn, gen_message(IRResultMsg(result=ir_result)))


def run_ir_server():
    """Run the image recognition server on the worker.

    This will get the task from the manager, perform image recognition on them,
    and return the result back to the manager
    """
    print("Preparing Server")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # start the server on the worker address given
        s.bind((WORKER_ADDRESS.ip, WORKER_ADDRESS.port))
        print("Server started on", WORKER_ADDRESS.ip,
              "port:", WORKER_ADDRESS.port)

        while True:
            s.listen()

            # successfully connected
            conn, addr = s.accept()
            ir_thread = threading.Thread(
                target=run_ir_protocol, args=(conn, addr)
            )
            ir_thread.start()


if __name__ == "__main__":
    run_ir_server()
