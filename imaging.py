import cv2
import numpy as np
from PIL import Image
from mss import mss
from abc import ABC, abstractmethod


class ImageSource(ABC):
    @abstractmethod
    def read(self):
        pass


class Camera(ImageSource):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)

    def read(self):
        _, frame = self.cam.read()
        _, buf = cv2.imencode('.jpg', frame)
        return buf


class Screen(ImageSource):
    def __init__(self):
        self.mss = mss()

    def read(self):
        with self.mss as sct:
            img = sct.grab(sct.monitors[0])
        nparray = np.array(img)
        _, buf = cv2.imencode('.jpg', nparray)
        return buf