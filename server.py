from multicast import MulticastServer
from imaging import Camera, Screen, NewScreen

srv = MulticastServer()

sources = [Camera, Screen, NewScreen]
for i, source in enumerate(sources):
    print('%i) %s (%s)' % (i+1, source.__name__, source.__doc__))

src = int(input('Select source: '))

source = sources[src-1]()

while True:
    buf = source.read()
    srv.send_bytes(buf)