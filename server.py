from multicast import MulticastServer
from imaging import Camera, Screen, NewScreen
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--group', default=1, help='Multicast group. By default it\'s 1', type=int)
parser.add_argument('--source', default=-1, help='Specify source(by default you need to do it interactively)', type=int)
args = parser.parse_args()


srv = MulticastServer(mcast_group=args.group)

sources = [Camera, Screen, NewScreen]
if args.source < 1:
    for i, source in enumerate(sources):
        print('%i) %s (%s)' % (i+1, source.__name__, source.__doc__))
    src = int(input('Select source: '))
else:
    src = args.source

source = sources[src-1]()

while True:
    buf = source.read()
    srv.send_bytes(buf)