from multicast import MulticastServer
from imaging import Camera, Screen

srv = MulticastServer()
sources = [Camera, Screen]
for i, source in enumerate(sources):
    print('%i) %s' % (i+1, source.__name__))

src = int(input('Select source: '))

source = sources[src-1]()

while True:
    buf = source.read()
    srv.send_bytes(buf)