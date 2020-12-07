from flask import Flask, request, url_for, render_template, jsonify, redirect
import os, sys, json, socket, random, time
from werkzeug.utils import secure_filename
import threading
import argparse

worker_tasks = dict()
task_lock = threading.Lock()
file_id = 0
file_id_lock = threading.Lock()


from website.setting import *
from src.interface import *

app = Flask(__name__)
app.secret_key = "cs655"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
worker_addresses = []

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # self-defined image id
    return render_template('index.html')


@app.route('/api/v1/classifier', methods=['POST'])
def classifier():
    result = "Empty File!"
    if 'file' not in request.files:
        return jsonify(result=result)
    file = request.files['file']
    if file.filename == '':
        return jsonify(result=result)

    if '.' in file.filename and file.filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS:
        suffix = file.filename.rsplit('.')[-1].lower()

        global worker_tasks
        global file_id
        global task_lock
        picked_worker = None
        min_num_tasks = sys.maxsize

        task_lock.acquire()
        # generate unique file id and pick the worker with minimum workload
        num_total_tasks = 0
        tied_workers = []
        for worker in worker_tasks:
            num_tasks = worker_tasks[worker]
            num_total_tasks += num_tasks
            if num_tasks < min_num_tasks:
                min_num_tasks = num_tasks
                picked_worker = worker
                tied_workers = []
            elif num_tasks == min_num_tasks:
                tied_workers.append(worker)

        if len(tied_workers) != 0:
            tied_workers.append(picked_worker)
            picked_worker = random.choice(tied_workers)
            if DEBUG:
                print("There is a tie when picking the worker among the worker list " + str(tied_workers) + ". A random worker will be picked from them.")
        if DEBUG:
            print("Worker Task Status:")
            for worker in worker_tasks:
                print(str(worker) + "\t" + str(worker_tasks[worker]))
            print("Assigning task to the worker " + str(worker))
        file_id_lock.acquire()
        if num_total_tasks == 0:
            file_id = 0
        file_id += 1
        file_id_lock.release()
        if DEBUG:
            print("New unique file id:" + str(file_id))
        filename = secure_filename(str(file_id) + '.' + suffix)
        if picked_worker == None:
            return jsonify(result=result)
        else:
            worker_tasks[picked_worker] += 1
        complete_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(complete_filepath)
        task_lock.release()


        try:
            time.sleep(5*random.random())
            result = image_recognition_with_worker(picked_worker, complete_filepath)
        except:
            result = "Recognition task failed!"

        task_lock.acquire()
        os.remove(complete_filepath)
        if worker_tasks[picked_worker] != 0:
            worker_tasks[picked_worker] -= 1
        task_lock.release()

    return jsonify(result=result)


def init_workers():
    global worker_tasks
    global worker_addresses
    for worker_addr in worker_addresses:
        worker_tasks[worker_addr] = 0


def isPortValid(port):
    return port >= 0 and port <= 65535


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-P','--port', type=int, help='port number',default=20000)
    parser.add_argument('--json_conf', help='the json filepath that contains worker addresses ', default="workers.json")
    args = parser.parse_args(argv)
    # check valid port number:
    _port = int(args.port)
    if not isPortValid(_port):
        print(_port)
        print("Invalid port number: port number should be between 0 and 65535")
        exit()
    if not os.path.exists(args.json_conf):
        print("Invalid json path!")
        exit()
    f = open(args.json_conf)
    conf = json.load(f)
    global worker_addresses
    for address in conf:
        if "ip" in address and "port" in address:
            if isPortValid(address["port"]):
                worker_addresses.append(Address(address["ip"],address["port"]))
            else:
                print("Invalid worker port number: port number should be between 0 and 65535")
                exit()
        else:
            print("Invalid json format: ip or port has to be specified for an address")
            exit()

    init_workers()
    print("Web starts")
    app.run(host= '0.0.0.0', debug=DEBUG, port=args.port, threaded=True)

if __name__ == '__main__':
    main(sys.argv[1:])
