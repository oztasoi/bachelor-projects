from package.constants import FAKE_UDP_PORT
import socket
import asyncio as aio

from .utils import sock_recvfrom
from .TCPPacket import TCPPacket


class TCPLayer():
    def __init__(self, src_port):
        super().__init__()
        assert src_port is not None

        self.handler_map = {}
        self.src_port = src_port
        assert self.src_port == FAKE_UDP_PORT

    def loop(self):
        aio.create_task(self.recv_loop())

    def attach_handler(self, addr, handler):
        print('tcp_layer:attach_handler:', addr, handler)
        assert self.handler_map.get(addr) is None
        self.handler_map[addr] = handler

    def detach_handler(self, addr):
        print('tcp_layer:detach_handler:', addr, self.handler_map[addr])
        assert self.handler_map.get(addr) is not None
        del self.handler_map[addr]

    async def recv_loop(self):
        print('tcp_layer:recv_loop start')
        print('tcp_layer:recv_loop:src_port', self.src_port)
        loop = aio.get_running_loop()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            sock.bind(('', self.src_port))
            sock.setblocking(False)

            while True:
                await aio.sleep(0.01)
                line, _ = await sock_recvfrom(loop, sock, TCPPacket.MAX_PACKET_SIZE)
                packet = TCPPacket.from_binary(line)
                print('tcp_layer:recv_loop:packet', packet)
                handler = self.handler_map.get(packet.dst_addr)
                if handler:
                    await handler(packet)
                else:
                    print("MISSING HANDLER!!!!", packet.dst_addr)