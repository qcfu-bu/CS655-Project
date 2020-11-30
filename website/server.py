from flask import Flask, request, url_for, render_template, jsonify, redirect
import os, sys, json, socket
from werkzeug.utils import secure_filename

from setting import *
from classifier_client import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
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
        filename = secure_filename(file.filename)
        complete_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(complete_filepath)
        result = classifier_client(complete_filepath)
        return jsonify(result=result)



if __name__ == '__main__':
	app.run(host= '0.0.0.0', debug=True, port=8080, threaded=True)
