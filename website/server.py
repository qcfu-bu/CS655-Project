from workers_management.manager import add_to_queue
from flask import Flask, request, url_for, render_template, jsonify, redirect, session
import os, sys, json, socket
from werkzeug.utils import secure_filename
import threading

from website.setting import *
from workers_management.manager import add_to_queue, find_result
from workers_management.manager import main as mfunc

app = Flask(__name__)
app.secret_key = "cs655"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # self-defined image id
    session['image_id'] = 1
    return render_template('index.html')


@app.route('/api/vi/classifier', methods=['POST'])
def classifier():
    result = "Empty File!"
    if 'file' not in request.files:
        return jsonify(result=result)
    file = request.files['file']
    if file.filename == '':
        return jsonify(result=result)

    if '.' in file.filename and file.filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS:
        suffix = file.filename.rsplit('.')[-1].lower()
        fileid = secure_filename(str(session.get('image_id')) + '.' + suffix)
        session['image_id'] += 1
        # complete_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        complete_id = os.path.join(app.config['UPLOAD_FOLDER'], fileid)
        # file.save(complete_filepath)
        file.save(complete_id)
        # send complete_id to manager
        add_to_queue(complete_id)
        result = find_result(complete_id)
        return jsonify(result=result)

def main():
    print("Web starts")
    app.run(host= '127.0.0.1', debug=True, port=20000, threaded=True)

if __name__ == '__main__':
    allocation = threading.Thread(target=mfunc)
    allocation.start()
    main()

