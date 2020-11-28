# CS655 Project
## Image Recognition

Members:
- Qiancheng Fu 
- Lina Qiu
- Cheng Zhang
- Zichen Zhu

### How to run

1. Make sure to use python version >= 3.6. Tested on Python 3.8.

### Updates

1. Nov-28-2020: Added `image-recognition` directory, and associated scripts and code. The image recognitizer is MobileNetV2 through TensorFlow 2.3. The program is separated into 2 parts, a daemon, and a client. The daemon is run on a worker node, performing image recognition. The client is run on the interface, performing preprocessing, and sending images to daemon through socket messages. The `scripts` subdirectory contain installers for both daemon and client. - **qcfu**

