from camera.camera_opencv import Camera
import cv2
from PIL import Image
from io import BytesIO
import numpy as np

def gen2(camera):
    """Returns a single image frame"""
    frame = camera.get_frame()
    yield frame

img = gen2(Camera)
curr_img = Image.open(BytesIO(img))
curr_img_cv2 = cv2.cvtColor(np.array(curr_img), cv2.COLOR_RGB2BGR)
curr_img_cv2.save('image')
