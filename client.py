from multicast import MulticastClient
import cv2
import numpy as np
clt = MulticastClient()

for frame in clt.read():
    nparr = np.fromstring(frame, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    cv2.imshow('Multistream', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
