import io
import numpy as np
import pickle
import base64

from PIL import Image

with open("./digits_model/model/clf.pickle", "rb") as f:
    clf = pickle.load(f)

with open("digit2.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

img = Image.open(io.BytesIO(base64.decodebytes(encoded_string)))
number = np.round((np.array(img)/255)*16)
print(clf.predict(number.reshape(1, -1)))
