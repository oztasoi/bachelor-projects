import struct
from collections import namedtuple
from ipaddress import ip_address

from bidict import bidict

from . import constants as Constants

import colorama as C

class TCPPacket(namedtuple('TCPPacket', 'src_addr dst_addr type index rwnd payload')):
    PACKET_HEADER_SIZE = 29  # in bytes
    MAX_PACKET_PAYLOAD_SIZE = 1471  # in bytes
    MAX_PACKET_SIZE = PACKET_HEADER_SIZE + MAX_PACKET_PAYLOAD_SIZE  # in bytes

    FORMAT = f"=IIiiciii{MAX_PACKET_PAYLOAD_SIZE}s"
    FORMAT_FIELDS = 'src_ip dst_ip src_port dst_port type index rwnd payload_length payload'

    type_map = bidict({
        'data': 0,
        'ack': 1,
        'window_probe_req': 2,
        'window_probe_res': 3,
        'ping': 4,
        'pong': 5,
        'connect': 6,
        'connect-ack': 7,
        'close': 8,
    })

    def __repr__(self):
        return C.Fore.BLUE + f"TCP {repr(self.type).ljust(7)} from {self.src_addr} to {self.dst_addr}, ix={self.index}: {repr(self.payload)}" + C.Style.RESET_ALL


    @staticmethod
    def from_binary(bytes):
        unpacked = struct.unpack(TCPPacket.FORMAT, bytes)
        src_ip, dst_ip, src_port, dst_port, type, index, rwnd, payload_length, payload = unpacked
        type = int.from_bytes(type, byteorder=Constants.BYTE_ORDER)
        return TCPPacket(
            (str(ip_address(src_ip)), src_port),
            (str(ip_address(dst_ip)), dst_port),
            TCPPacket.type_map.inverse[type],
            index,
            rwnd,
            payload[:payload_length]
        )

    def to_binary(self):
        src_ip, src_port = self.src_addr
        dst_ip, dst_port = self.dst_addr
        return struct.pack(TCPPacket.FORMAT,
                           int(ip_address(src_ip)),  # format ip as 32 bit
                           int(ip_address(dst_ip)),  # format ip as 32 bit
                           src_port,
                           dst_port,
                           TCPPacket.type_map[self.type].to_bytes(1, byteorder=Constants.BYTE_ORDER),
                           self.index,
                           self.rwnd,
                           len(self.payload),
                           self.payload)
