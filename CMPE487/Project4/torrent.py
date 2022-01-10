from package.constants import BYTE_ORDER, FAKE_UDP_PORT, ONE_MEGABYTE, REAL_UDP_PORT
from package.TCPSocket import TCPSocket
from package.TCPLayer import TCPLayer
from package.utils import send_broadcast_udp_packet, send_udp_packet, sock_recvfrom, sock_sendto, argmin
from json.decoder import JSONDecodeError
from collections import defaultdict
from functools import reduce
import socket
import os
import hashlib
from bidict import bidict
import asyncio as aio
from aioconsole import ainput as async_input
import sys
import hashlib
import json
import colorama as C

tcp_payload_type_mapper = bidict({ 'json': 0, 'binary': 1 })

my_ip = sys.argv[1]
torrent_dir = sys.argv[2]

class Torrent:

    CHUNK_SIZE = ONE_MEGABYTE
    UDP_PACKET_SIZE = 1500

    def __init__(self, my_udp_addr, my_tcp_addr, torrent_dir) -> None:
        super().__init__()
        self.my_tcp_addr = my_tcp_addr
        self.my_udp_addr = my_udp_addr
        self.torrent_dir = torrent_dir
        self.my_manifest = defaultdict()
        self.revealed_manifests = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

        # revealed_manifests format
        # {
        #     "file_1": {
        #         "chunk_count": 23
        #         "ip_1": {
        #             0: "...hash...",
        #             1: "hash...",
        #             2: "hash...",

        #         },
        #         "ip_2": {
        #             0: "...hash...",
        #             1: "hash...",
        #         },
        #     }
        # }

        # my_manifest
        # {
        #     "file_name": {
        #         "chunk_count": 23,
        #         "self": "<file_hash>",
        #         0: "<chunk_hash>",
        #         1: "<chunk_hash>",
        #         .
        #         .
        #         .
        #     }
        # }

        # received manifest format
        # {
        #     "file1_name": {
        #         1: "...hash",
        #     }

        # }

    def update_manifest(self):
        with open(f"{self.torrent_dir}/manifest.json", "r") as manifest_file:
            old_manifest = json.load(manifest_file)

            if hashlib.sha256(bytes(old_manifest)) == hashlib.sha256(bytes(self.manifest)):
                return

            self.my_manifest = defaultdict()
            file_list = sorted(list(os.listdir(self.torrent_dir)))
            for file in file_list:
                self.hash_file(file)

    def dump_manifest(self):
        with open(f"{self.torrent_dir}/manifest.json", "w") as manifest_file:
            manifest_file.write(json.dumps(self.my_manifest))
            manifest_file.flush()

    def hash_file(self, file_name, file_path=False):
        sha256 = hashlib.sha256()
        chunk_hash_dict = {}
        file_identifier = file_name if file_path else f"{self.torrent_dir}/{file_name}"
        with open(file_identifier, 'rb') as fstream:
            chunk_ix = 0
            bs = b''
            while True:
                bs = fstream.read(Torrent.CHUNK_SIZE)
                if not bs:
                    break
                chunk_hash_dict[chunk_ix] = hashlib.sha256(bs).hexdigest()
                sha256.update(bs)
                chunk_ix += 1

        chunk_hash_dict["self"] = sha256.hexdigest()
        chunk_hash_dict["chunk_count"] = chunk_ix
        self.my_manifest[file_name] = chunk_hash_dict

    def get_missing_chunks(self, file_name):
        current_file = self.my_manifest[file_name]
        missing_chunk_ids = [ix for ix in range(self.revealed_manifests[file_name]
                                                ["chunk_count"]) if ix not in set(current_file.keys())]
        return missing_chunk_ids

    def get_ips_for_chunks(self, file_name: str,  missing_chunks: list):
        total_recipe = {missing_chunk: set() for missing_chunk in missing_chunks}
        for src_ip, src_chunks in self.revealed_manifests[file_name].items():
            for src_chunk in src_chunks:
                total_recipe[src_chunk].add(src_ip)

        return total_recipe

    def get_final_ip_for_chunks(self, ips_of_chunks):
        ip_for_chunk = {}
        ip_use_count = defaultdict(int)
        for chunk, ips in ips_of_chunks:
            # select ip from ips which minimizes ip_count
            ip_with_min_use = argmin(ips, lambda ip: ip_use_count[ip])
            ip_for_chunk[chunk] = ip_with_min_use

        return ip_for_chunk

    def prepare_recipe(self, file_name: str):
        if file_name not in self.revealed_manifests:
            print(file_name, 'does not exist.')
            return

        missing_chunks = self.get_missing_chunks(file_name)
        ips_for_chunks = self.get_ips_for_chunks(file_name, missing_chunks)
        final_ip_for_chunks = self.get_final_ip_for_chunks(ips_for_chunks)

        chunks_for_final_ips = defaultdict(list)
        for chunk, ip in final_ip_for_chunks:
            chunks_for_final_ips[ip].append(chunk)

        return chunks_for_final_ips

    async def read_tcp_message(self, tcp_socket: TCPSocket):
        message = b''
        packet = None
        async for _, packet in tcp_socket.read():
            message += packet.payload
        return (message, packet.src_addr, packet.dst_addr)

    async def send_tcp_message(self, message, dst_addr):
        tcp_socket = TCPSocket(self.tcp_layer)
        tcp_socket.loop()
        print("send_tcp_message: trying to connect", message, dst_addr)
        await tcp_socket.connect(self.my_tcp_addr, dst_addr)

        print(C.Fore.RED + 'send_tcp_message:', message, dst_addr, C.Style.RESET_ALL)
        message = json.dumps(message).encode("utf-8")
        await tcp_socket.send(message)
        await tcp_socket.send_close()

    async def send_tcp_chunk(self, chunk: bytes, dst_addr):
        tcp_socket = TCPSocket(self.tcp_layer)
        tcp_socket.loop()
        print(C.Fore.RED + 'send_tcp_chunk:', chunk, dst_addr, C.Style.RESET_ALL)
        await tcp_socket.connect(self.my_tcp_addr, dst_addr)
        await tcp_socket.send(chunk)
        await tcp_socket.send_close()
        

    async def handle_udp_message(self, line):
        message = json.loads(line.decode('utf-8').strip())
        if message['src']['ip'] == self.my_udp_addr[0]:
            print('handle_udp_message: ignore echo')
            return

        print(C.Fore.GREEN + 'handle_udp_message:', message, C.Style.RESET_ALL)
        if message['type'] == 'manifest_req':
            # we need to send our own manifest
            manifest_res = {
                'type': 'manifest_res',
                'src': {
                    'ip': self.my_tcp_addr[0],
                    'udp_port': self.my_udp_addr[1],
                    'tcp_port': self.my_tcp_addr[1]
                },
                'payload': self.my_manifest
            }
            await self.send_tcp_message(manifest_res, (message['src']['ip'], message['src']['tcp_port']))

    async def handle_tcp_message(self, message: bytes, src_addr, dst_addr):
        # the message is a JSON
        message = message.decode('utf-8')
        message = json.loads(message)
        print(C.Fore.GREEN + 'handle_tcp_message:', message, src_addr, dst_addr, C.Style.RESET_ALL)

        if message['type'] == 'manifest_res':
            # we need to update our manifest of other people's files
            manifest = message['payload']
            for file_name, file_chunks in manifest.items():
                if "chunk_count" in file_chunks:
                    self.revealed_manifests[file_name]["chunk_count"] = file_chunks.pop("chunk_count")
                self.revealed_manifests[file_name][src_addr[0]].update(file_chunks)

    async def tcp_recv_loop(self):
        print('tcp_recv_loop:start')
        while True:
            tcp_socket = TCPSocket(self.tcp_layer)
            tcp_socket.loop()
            tcp_socket.bind(self.my_tcp_addr)

            message, src_addr, dst_addr = await self.read_tcp_message(tcp_socket)
            # message can either be JSON or BINARY !!
            await self.handle_tcp_message(message, src_addr, dst_addr)
            await aio.sleep(0.2)
            # await tcp_socket.disconnect()
            print("tcp recv loop: END")

    async def udp_recv_loop(self):
        print("udp_recv_loop:start")
        loop = aio.get_running_loop()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', self.my_udp_addr[1]))
            sock.setblocking(False)

            while True:
                await aio.sleep(0.01)
                line, _ = await sock_recvfrom(loop, sock, Torrent.UDP_PACKET_SIZE)
                await self.handle_udp_message(line)


    async def broadcast_manifest_req(self):
        message = {
            'src': {
                # 'name': sys.argv[2],
                'ip': self.my_tcp_addr[0],
                'udp_port': self.my_udp_addr[1],
                'tcp_port': self.my_tcp_addr[1]
            },
            'type': 'manifest_req',
        }

        print('broadcast_manifest_req:', message)
        # await send_broadcast_udp_packet(('<broadcast>', self.my_tcp_addr[0] - 1), json.dumps(message))
        #for i in range(2):
        await send_broadcast_udp_packet(('25.255.255.255', self.my_udp_addr[1]), json.dumps(message).encode('utf-8'))

    async def handle_command(self, command):
        if command == 'my manifest':  # show my manifest
            print("My manifest:")
            print(json.dumps(dict(self.my_manifest), indent=4))
        elif command == 'ask manifests':  # show my manifest
            print("Asking for manifests...")
            await self.broadcast_manifest_req()
            print("Finished asking for manifests, waiting for their response...")
            # ... wait like 3 seconds?
            await aio.sleep(5)
            print(json.dumps(dict(self.revealed_manifests), indent=4))

        elif command == 'show other files':  # show all files of other people, even incomplete
            print("Other files:")
            # print(json.dumps(dict(self.), indent=4))
        elif command == 'upload file':
            file_path = await async_input('enter path to the file:')
            self.hash_file(file_path, file_path=True)

        else:
            print('unknown command:', command)

    async def retrieve_chunks(self, file_name):
        recipe = self.prepare_recipe(file_name)

        final_chunks = {}

        async def recv_loop(port, chunk_count: int):
            print(f'recv_loop: {port=} {chunk_count=}')
            tcp_socket = TCPSocket(self.tcp_layer)
            tcp_socket.loop()
            tcp_socket.bind((self.my_tcp_addr[0], port))

            message = b''
            async for _, packet in tcp_socket.read():
                message += packet.payload

            for i in range(chunk_count):
                base = i*Torrent.CHUNK_SIZE
                msg = message[base: base+Torrent.CHUNK_SIZE]
                chunk_ix = int.from_bytes(msg[:4], byteorder=BYTE_ORDER)
                chunk_length = int.from_bytes(msg[4:8], byteorder=BYTE_ORDER)
                chunk_bytes = msg[8:8+chunk_length]
                final_chunks[chunk_ix] = chunk_bytes

        tasks = []
        async for ix, (chunk_ip, chunk_ixs) in enumerate(recipe.items()):
            ask_for_chunks = {
                'type': 'ask_chunks',
                'src': {
                    # 'name': sys.argv[2],
                    'ip': self.my_tcp_addr[0],
                    'udp_port': self.my_udp_addr[1],
                    'tcp_port': self.my_tcp_addr[1]
                },
                'payload': {
                    'file_name': file_name,
                    'chunks': chunk_ixs,
                }
            }
            dst_addr = (chunk_ip, ix + 1 + FAKE_UDP_PORT)
            await self.send_tcp_message(ask_for_chunks, dst_addr)
            tasks.append(recv_loop(dst_addr[1], len(chunk_ixs)))

        await aio.wait(*tasks)
        self.process_chunks(file_name, final_chunks)

        # we have all chunks

    def process_chunks(self, file_name: str, final_chunks: dict):
        hashed_chunks = {chunk_id: hashlib.sha256(chunk_bytes).hexdigest()
                         for chunk_id, chunk_bytes in final_chunks.items()}
        self.my_manifest[file_name].update(hashed_chunks)
        self.my_manifest[file_name]["chunk_count"] = self.revealed_manifests[file_name]["chunk_count"]
        # what about file hash?

        with open(f'{self.torrent_dir}/{file_name}', "wb") as file:
            for chunk_id, chunk_bytes in final_chunks:
                offset = chunk_id * Torrent.CHUNK_SIZE
                file.seek(offset)
                file.write(chunk_bytes)
    
    def loop(self):
        aio.create_task(self.tcp_recv_loop())
        aio.create_task(self.udp_recv_loop())

    async def main(self):
        self.tcp_layer = TCPLayer(FAKE_UDP_PORT) 
        self.tcp_layer.loop()
        self.loop()

        try:
            while True:
                command = await async_input(">>> ")
                await self.handle_command(command)
        except KeyboardInterrupt:
            print("Bye!")


if __name__ == "__main__":
    torrent = Torrent(
        my_udp_addr=(my_ip, REAL_UDP_PORT),
        my_tcp_addr=(my_ip, FAKE_UDP_PORT),
        torrent_dir=torrent_dir
    )
    aio.run(torrent.main())
