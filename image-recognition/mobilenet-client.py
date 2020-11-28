import os
import socket
import struct
import json
import numpy as np

from PIL import Image

TCP_IP = 'localhost'
TCP_PORT = 5001

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

local_dir = "img"
files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(
    local_dir) for f in filenames]


def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)
    return d


for file in files:
    img = Image.open(file)
    img = img.resize((224, 224))

    data = np.asarray(img, dtype='float32').reshape((224, 224, 3))
    data = data.tostring()
    size = len(data)

    sock.sendall(struct.pack(">L", size) + data)

    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: ", payload_size)
    while len(data) < payload_size:
        data += sock.recv(4096)
    print("Done Recv: ", len(data))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: ", msg_size)
    while len(data) < msg_size:
        data += sock.recv(4096)
    data = data[:msg_size]

    prediction = binary_to_dict(data)
    print(prediction)

sock.close()
