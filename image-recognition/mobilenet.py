import pathlib
import numpy as np
import os

from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions


image_dir = pathlib.Path('img')
files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(
    image_dir) for f in filenames]

image_data = []
for file in files:
    img = load_img(file, target_size=(224, 224))
    data = img_to_array(img)
    data = np.expand_dims(data, 0)
    data = keras.applications.mobilenet_v2.preprocess_input(data)
    image_data.append(data)

model = keras.applications.MobileNetV2(weights='imagenet')

for data in image_data:
    prediction = model.predict(data)
    label = decode_predictions(prediction, 5)
    print(label)
