from multicast import MulticastClient
import cv2
import numpy as np


clt = MulticastClient()


while True:
    frame = b''
    for fr in clt.read():
        frame += fr
    nparr = np.fromstring(frame, np.uint8)
    try:
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        cv2.imshow('Multistream', img)
    except cv2.error:
        pass
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
