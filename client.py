from multicast import MulticastClient
import cv2
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-g', '--group', default=1, help='Multicast group. By default it\'s 1', type=int)
args = parser.parse_args()


clt = MulticastClient(args.group)


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
