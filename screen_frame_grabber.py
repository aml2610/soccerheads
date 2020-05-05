from PIL import ImageGrab
import numpy as np


def grab_screen_frame(bbox):
    frame = ImageGrab.grab(bbox).convert("RGB")
    return np.array(frame)
