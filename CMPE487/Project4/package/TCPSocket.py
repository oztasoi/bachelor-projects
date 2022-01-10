import json
import socket
import asyncio as aio
from collections import defaultdict
import sys

from .TCPLayer import TCPLayer
from .TCPPacket import TCPPacket 
from .utils import chunker, sock_sendto
from .constants import BYTE_ORDER, FAKE_UDP_PORT, MAX_BUFFER_SIZE, MIN_WINDOW

port_map = dict()

class TCPSocket():
    WINDOW_PROBE_TIMEOUT = 4  # in seconds
    ACK_TIME_LIMIT = 1  # in seconds
    PING_TIME_LIMIT = 3  # in seconds

    def __init__(self, tcp_layer: TCPLayer):
        super().__init__()
        self.id = hex(id(self))
        print(self.id, 'TCPSocket __init__')
        self.tcp_layer = tcp_layer
        self.index = 0
        self.unacked = {}
        self.acked = {}
        self.recv = {}
        self.remaining_buffer_space_here = MAX_BUFFER_SIZE
        self.remaining_buffer_space_there = MAX_BUFFER_SIZE
        self.last_read_index = -1
        self.try_count = defaultdict(int)
        self.ping_count = 0
        self.is_connected = False
        self.received_connect = False
        self.received_connect_ack = False
        self.my_addr = None
        self.other_addr = None

    def loop(self):
        aio.create_task(self.send_unacked_loop())
        #aio.create_task(self.send_ping_loop())

    async def disconnect(self):
        print(self.id, 'disconnect:', self.my_addr)
        self.tcp_layer.detach_handler(self.my_addr)
        self.is_connected = False
        self.received_connect = False
        self.received_connect_ack = False
        self.socket_mode = None
        self.my_addr = None
        self.other_addr = None

    # async def unbind(self):
    #     print(self.id, 'unbind:', self.my_addr)
    #     self.tcp_layer.detach_handler(self.my_addr)
    #     self.socket_mode = None
    #     self.my_addr = None

    def bind(self, my_addr):
        print(self.id, 'bind:', my_addr)
        self.socket_mode = 'bind'
        self.my_addr = my_addr
        self.tcp_layer.attach_handler(self.my_addr, self.handle_recv)

    async def send_close(self):
        await self.send_packet(('close', -1, self.remaining_buffer_space_here, b''))
        await self.disconnect()

    async def connect(self, my_addr, other_addr):
        if len(port_map) == 0:
            port_map[self.id] = 6000
        else:
            port_map[self.id] = max(port_map.values()) + 1

        my_addr = (my_addr[0], port_map[self.id])
        print(self.id, 'connect:', other_addr)
        self.socket_mode = 'connect'
        self.my_addr = my_addr
        self.other_addr = other_addr
        self.tcp_layer.attach_handler(self.my_addr, self.handle_recv)

        ack_tries = 0
        while not self.received_connect_ack:
            print(self.id, 'connect:ack_tries', ack_tries, self.received_connect_ack)
            if ack_tries > 3:
                raise ConnectionError

            await self.send_packet(('connect', - 1, self.remaining_buffer_space_here, b''))
            ack_tries += 1
            await aio.sleep(TCPSocket.ACK_TIME_LIMIT)

        # at this point we have received connect ack
        time_elapsed = 0
        while not self.received_connect:
            await aio.sleep(0.01)
            time_elapsed += 0.01

            if time_elapsed > 3:
                raise ConnectionError

        # at this point 3-way handshake done
        self.is_connected = True
        print(self.id, 'connect:is_connected', self.is_connected)

    async def handle_recv(self, packet):
        print(self.id, 'handle_recv:', packet)

        self.remaining_buffer_space_there = packet.rwnd
        if packet.type == 'connect':
            self.other_addr = packet.src_addr
            await self.send_packet(('connect-ack', - 1, self.remaining_buffer_space_here, b''))
            if not self.received_connect:
                self.received_connect = True
                await self.send_packet(('connect', - 1, self.remaining_buffer_space_here, b''))
        elif packet.type == 'connect-ack':
            self.received_connect_ack = True
            if self.socket_mode == 'bind':
                self.is_connected = True
        elif packet.type == 'close':
            self.is_connected = False
            self.disconnect()

        if self.is_connected:
            if packet.type == 'window_probe_req':
                await self.send_packet(('window_probe_res', -1, self.remaining_buffer_space_here, b''))
            elif packet.type == 'window_probe_res': # changing remain_buffer_space_there already done
                pass
            elif packet.type == 'ack':
                acked_packet_index = int.from_bytes(packet.payload, byteorder=sys.byteorder)
                if acked_packet_index in self.unacked.keys():
                    acked_packet = self.unacked[acked_packet_index]
                    del self.unacked[acked_packet_index]
                    self.acked[acked_packet_index] = (self.other_addr, acked_packet)
            elif packet.type == 'pong':
                self.ping_count = 0
            elif packet.type == 'ping':
                print("sending pong...")
                await self.send_packet(('pong', -1, self.remaining_buffer_space_here, b''))
            elif packet.type == 'data':
                print(self.id, 'recv:data:', self.other_addr, packet)

                if packet.index > self.last_read_index:
                    self.recv[packet.index] = (self.other_addr, packet)
                    self.remaining_buffer_space_here -= TCPPacket.MAX_PACKET_SIZE

                await self.send_packet(('ack', -1, self.remaining_buffer_space_here, packet.index.to_bytes(4, byteorder=BYTE_ORDER)))
            
    async def send_ping_loop(self):
        # return
        while not self.is_connected:
            await aio.sleep(0.05)

        while self.is_connected:
            # print(self.id, 'send_ping_loop', self.ping_count)
            self.ping_count += 1
            await aio.sleep(TCPSocket.PING_TIME_LIMIT)
            await self.send_packet(('ping', -1, self.remaining_buffer_space_here, b''))

    def chunk_data(self, data):
        return chunker(data, TCPPacket.MAX_PACKET_PAYLOAD_SIZE)

    async def send_packet(self, packet_args):
        # 'TCPPacket', 'src_addr dst_addr type index rwnd payload'
        packet = packet_args
        if not isinstance(packet_args, TCPPacket):
            assert self.my_addr 
            assert self.other_addr
            packet = TCPPacket(self.my_addr, self.other_addr, *packet_args)

        packet = packet._replace(rwnd=self.remaining_buffer_space_here)

        print(self.id, 'send_packet:', packet)

        loop = aio.get_running_loop()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setblocking(False)
            #sock.bind(('', 0))

            # print('send_packet:self.other_addr', self.other_addr)
            await sock_sendto(loop, sock, packet.to_binary(), (self.other_addr[0], FAKE_UDP_PORT))

    async def send_unacked_loop(self):
        while not self.is_connected:
            await aio.sleep(0.05)

        while self.is_connected:
            await aio.sleep(TCPSocket.ACK_TIME_LIMIT)

            if self.unacked:
                print(self.id, 'send_unacked_loop:', list(self.unacked.keys()), self.remaining_buffer_space_there)

            unacked_list = list(self.unacked.items())

            for ix, (_, packet) in unacked_list:
                if ix not in self.unacked:
                    continue

                while self.remaining_buffer_space_there < MIN_WINDOW:
                    print(self.id, f'send_unacked_loop: {self.remaining_buffer_space_there} < MIN_WINDOW')
                    await aio.sleep(TCPSocket.WINDOW_PROBE_TIMEOUT)
                    await self.send_packet(('window_probe_req', -1, self.remaining_buffer_space_here, b''))

                self.try_count[packet.index] += 1
                await self.send_packet(packet)

    async def send(self, data):
        """
        data: bytes
        addr: (ip, port) tuple
        """

        try:
            print(self.id, 'send start')
            chunks = self.chunk_data(data)
            # print(self.id, 'send data_chunks', chunks)

            packet_ixs = []

            for chunk in chunks:
                packet = TCPPacket(self.my_addr, self.other_addr, 'data', self.index,
                                self.remaining_buffer_space_here, chunk)
                packet_ixs.append(packet.index)

                while self.remaining_buffer_space_there < MIN_WINDOW:
                    print(self.id, f'send: {self.remaining_buffer_space_there} < MIN_WINDOW')
                    await aio.sleep(TCPSocket.WINDOW_PROBE_TIMEOUT)
                    await self.send_packet(('window_probe_req', -1, self.remaining_buffer_space_here, b''))

                await self.send_packet(packet)
                self.unacked[packet.index] = (self.other_addr, packet)
                self.index += 1

            while self.is_connected:
                print(self.id, 'check', set(packet_ixs).difference(set(self.acked.keys())))

                if len(self.try_count) and max(self.try_count.values()) > 3:
                    self.is_connected = False
                    await self.send_close()
                    raise ConnectionError

                if set(packet_ixs).issubset(set(self.acked.keys())):
                    for ix in packet_ixs:
                        del self.acked[ix]
                    break

                await aio.sleep(0.1)

        except KeyboardInterrupt:
            self.is_connected = False
            await self.send_close()
            raise KeyboardInterrupt

    async def read(self):
        while not self.is_connected:
            await aio.sleep(0.05)
        print(self.id, 'read start')

        try:
            while self.is_connected:
                if self.ping_count > 3:
                    self.is_connected = False
                    await self.send_close()
                    raise ConnectionError

                if len(self.recv) == 0:
                    await aio.sleep(0.05)
                    continue

                min_index = min(self.recv.keys())
                if min_index == self.last_read_index + 1:
                    addr, packet = self.recv[min_index]
                    del self.recv[min_index]
                    self.last_read_index += 1
                    self.remaining_buffer_space_here += TCPPacket.MAX_PACKET_SIZE

                    yield (addr, packet)
        except KeyboardInterrupt:
            self.is_connected = False
            await self.send_close()
            raise KeyboardInterrupt
