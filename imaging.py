import cv2
import numpy as np
from mss import mss
from abc import ABC, abstractmethod
import sys
if sys.platform in ('win32', 'darwin'):
    from PIL import ImageGrab as ig


class ImageSource(ABC):
    @abstractmethod
    def read(self):
        pass


class Camera(ImageSource):
    """Web-cam using CV2"""
    def __init__(self):
        self.cam = cv2.VideoCapture(0)

    def read(self):
        _, frame = self.cam.read()
        _, buf = cv2.imencode('.jpg', frame, (cv2.IMWRITE_JPEG_QUALITY, 90))
        return buf


class Screen(ImageSource):
    """Screen using MSS"""
    def __init__(self):
        self.mss = mss()

    def read(self):
        with self.mss as sct:
            img = sct.grab(sct.monitors[0])
        nparray = np.uint8(np.array(img.pixels))
        img = cv2.cvtColor(nparray, cv2.COLOR_BGRA2RGB)
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        _, buf = cv2.imencode('.jpg', img, (cv2.IMWRITE_JPEG_QUALITY, 50))
        return buf


class NewScreen(ImageSource):
    """Screen using ImageGrab(Win & Mac only)"""
    def read(self):
        screen = ig.grab()
        nparray = np.array(screen)
        _, buf = cv2.imencode('.jpg', nparray, (cv2.IMWRITE_JPEG_QUALITY, 50))
