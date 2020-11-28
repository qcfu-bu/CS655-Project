import socket
import struct
import threading
import json
import numpy as np

from tensorflow import keras
from tensorflow.keras.applications.imagenet_utils import decode_predictions


model = keras.applications.MobileNetV2(weights='imagenet')


def predict(data):
    """"make predictions with MobileNetV2"""
    data = data.copy()
    data = np.expand_dims(data, 0)
    data = keras.applications.mobilenet_v2.preprocess_input(data)

    prediction = model.predict(data)
    prediction = decode_predictions(prediction, 5)[0]

    result = {}
    for pred in prediction:
        result[pred[1]] = str(pred[2])

    return result


TCP_IP = 'localhost'
TCP_PORT = 5001


def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in str)
    binary = bytearray(binary.encode('utf8'))
    return binary


def handle(conn, addr):
    print("request from: ", addr[0])
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: ", payload_size)
    while len(data) < payload_size:
        data += conn.recv(4096)
    print("Done Recv: ", len(data))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: ", msg_size)
    while len(data) < msg_size:
        data += conn.recv(4096)
    data = data[:msg_size]

    data = np.frombuffer(
        data, dtype='float32').reshape((224, 224, 3))

    prediction = predict(data)
    data = dict_to_binary(prediction)
    size = len(data)

    conn.sendall(struct.pack('>L', size) + data)

    print("----------------------------------------")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)


while True:
    conn, addr = s.accept()
    threading._start_new_thread(handle, (conn, addr))
