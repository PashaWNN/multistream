import socket
import struct


class MulticastServer:
    PACKET_SIZE = 4096
    IP_SERVER = "224.1.1.%i"
    SERVER_PORT = 9090
    MULTICAST_TTL = struct.pack('b', 2)

    def __init__(self, mcast_group: int = 1):
        self.group = mcast_group
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.MULTICAST_TTL)

    def _create_packets(self, data: bytes):
        chunks = [data[i:i + self.PACKET_SIZE] for i in range(0, len(data), self.PACKET_SIZE)]
        result = [str(len(chunks)).encode('utf8')] + chunks
        return result

    def send_bytes(self, data: bytes):
        for packet in self._create_packets(data):
            self.sock.sendto(packet, (self.IP_SERVER % self.group, self.SERVER_PORT))


class MulticastClient:
    SERVER_IP = "224.1.1.%i"
    SERVER_PORT = 9090
    SOCKET_TIMEOUT = 10
    PACKET_SIZE = 8192

    def __init__(self, mcast_group: int = 1):
        self.group = mcast_group
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(self.SOCKET_TIMEOUT)
        self.sock.bind(('', self.SERVER_PORT))
        mreq = struct.pack('4sl', socket.inet_aton(self.SERVER_IP % self.group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.buffer = b''

    def _wait_sizedef(self):
        size = 0
        while not size:
            data = self.sock.recv(self.PACKET_SIZE)
            try:
                if data.decode('utf8').isdecimal():
                    size = int(data.decode('utf8'))
            except UnicodeDecodeError:
                pass
        return size

    def read(self):
        size = self._wait_sizedef()
        for i in range(size):
            yield self.sock.recv(self.PACKET_SIZE)


