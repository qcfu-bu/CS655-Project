# CS655 Project
## Image Recognition

Members:
- Qiancheng Fu
- Lina Qiu
- Cheng Zhang
- Zichen Zhu

### How to run

1. Make sure to use python version >= 3.6. Tested on Python 3.8.
2. Make sure the newest Flask is installed (`pip install Flask`)
3. At root dir, run `source bin/activate && pip install -e .`
4. On the server
    1. run `python website/server.py`
5. On each worker
    1. run `python src/worker.py`

### Updates

1. **Nov-28-2020**: Added `image-recognition` directory, and associated scripts and code. The image recognitizer is MobileNetV2 through TensorFlow 2.3. The program is separated into 2 parts, a daemon, and a client. The daemon is run on a worker node, performing image recognition. The client is run on the interface, performing preprocessing, and sending images to daemon through socket messages. The `scripts` subdirectory contain installers for both daemon and client. - **qcfu**

2. **Nov-29-2020**: Added `website` directory. To run the server locally, you can go to the website directory and run `python server.py`. Then you can visit localhost:8080 through your browser and upload any image. The port number can be specified by <code>app.run(port=[your port number])"</code> in `server.py`. Uploaded images will be saved under `website/uploaded_files` directory. The web server will call a function <code>classifier\_client(filename)</code> function which takes the image path as the input and returns a dictionary containing each possible object type with corresponding probability - **zczhu**

2. **Dec-5-2020**: Integrate `manager.py` into `website` && Added `exp` directory. To run the experiment scripts after you set up the system, you can run go to the `exp` directory and run `python exp.py`. Detailed usage can be found with `python exp.py --help` - **zczhu**
