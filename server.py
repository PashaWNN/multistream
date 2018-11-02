from multicast import MulticastServer
import cv2

srv = MulticastServer()

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()
    _, buf = cv2.imencode('.jpg', frame)
    srv.send_bytes(buf)