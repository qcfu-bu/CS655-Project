from flask import Flask, request, url_for, render_template, jsonify, redirect
import os, sys, json, socket, random, time
from werkzeug.utils import secure_filename
import threading

worker_tasks = dict()
task_lock = threading.Lock()


from website.setting import *
from src.shared import WORKER_ADDRESSES
from src.interface import *

app = Flask(__name__)
app.secret_key = "cs655"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        picked_worker = None
        min_num_tasks = sys.maxsize

        task_lock.acquire()
        # generate unique file id and pick the worker with minimum workload
        num_total_tasks = 0
        for worker in worker_tasks:
            num_tasks = worker_tasks[worker]
            num_total_tasks += num_tasks
            if num_tasks < min_num_tasks:
                num_tasks = min_num_tasks
                picked_worker = worker
        if DEBUG:
            print("New unique file id:" + str(num_total_tasks))
        filename = secure_filename(str(num_total_tasks+1) + '.' + suffix)
        if picked_worker == None:
            return jsonify(result=result)
        else:
            worker_tasks[worker] += 1
        complete_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(complete_filepath)
        task_lock.release()



        try:
            #time.sleep(5*random.random())
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
    for worker_addr in WORKER_ADDRESSES:
        worker_tasks[worker_addr] = 0


def main():
    init_workers()
    print("Web starts")
    app.run(host= '127.0.0.1', debug=DEBUG, port=20000, threaded=True)

if __name__ == '__main__':
    main()
