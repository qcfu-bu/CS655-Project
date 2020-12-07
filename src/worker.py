import socket
import threading
import uuid

from src.logging_util import Logger
from src.socket_util import receive_file_from, send_msg_to, receive_msg_from
from src.types import IRResult, Address, gen_message, IRResultMsg, parse_task_assign_msg, SuccessRespondMsg

from tensorflow import keras
from tensorflow.keras.applications.imagenet_utils import decode_predictions

from PIL import Image
import numpy as np


# init the worker logger
LOGGER = Logger(logging_from="WORKER")

# the address of current worker
# if it is localhost then it is for testing
WORKER_ADDRESS = Address("127.0.0.1", 65000)

model = keras.applications.MobileNetV2(weights='imagenet')


def image_recognition(file_name: str) -> IRResult:
    """Perform the image recognition on the given file

    :param file_name: the name of the file to recognize
    """

    img = Image.open(file_name)
    img = img.resize((224, 224))

    data = np.asarray(img, dtype='float32').reshape((224, 224, 3))

    data = np.expand_dims(data, 0)
    data = keras.applications.mobilenet_v2.preprocess_input(data)

    prediction = model.predict(data)
    prediction = decode_predictions(prediction, 5)[0]

    result = {}
    for pred in prediction:
        result[pred[1]] = str(pred[2])

    return result


def run_ir_protocol(conn: socket.socket) -> None:
    """perform the image recognition protocol with the manager

    :param conn: the connection to the manager
    """
    with conn:
        LOGGER.info("connected, executing IR"),

        LOGGER.info("receiving the task assignment message")
        # receive information about this task assignment
        task_assign_msg_str = receive_msg_from(conn)
        task_assign_msg = parse_task_assign_msg(task_assign_msg_str)
        # get the file name for the task file
        file_name = task_assign_msg.file_name

        LOGGER.info("sending success response")
        # indicate successfully get the file name
        send_msg_to(conn, gen_message(SuccessRespondMsg()))

        LOGGER.info(f"receiving the image file, saving to {file_name}")
        # generate a unique file name to save the file
        receive_file_from(conn, file_name)

        # do image recognition
        ir_result = image_recognition(file_name)
        LOGGER.info(f"obtained image recognition result {ir_result}")

        LOGGER.info("sending image recognition result")
        # send the result
        send_msg_to(conn, gen_message(IRResultMsg(result=ir_result)))

        LOGGER.info("protocol finished, disconnect")


def run_ir_server():
    """Run the image recognition server on the worker.

    This will get the task from the manager, perform image recognition on them,
    and return the result back to the manager
    """
    LOGGER.info("Preparing Server")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # start the server on the worker address given
        s.bind((WORKER_ADDRESS.ip, WORKER_ADDRESS.port))
        LOGGER.info(f"Server started on "
                    f"{WORKER_ADDRESS.ip}:{WORKER_ADDRESS.port}")

        while True:
            s.listen()

            # successfully connected
            conn, addr = s.accept()
            ir_thread = threading.Thread(
                target=run_ir_protocol, args=(conn,)
            )
            ir_thread.start()


if __name__ == "__main__":
    run_ir_server()
