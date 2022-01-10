import socket
import asyncio as aio

PORT = 5000

def sock_recvfrom(loop, sock, n_bytes, fut=None, registed=False):
    """
    CREDITS TO https://pysheeet-kr.readthedocs.io/ko/latest/notes/python-asyncio.html#simple-asyncio-udp-echo-server 
    """
    fd = sock.fileno()
    if fut is None:
        fut = loop.create_future()
    if registed:
        loop.remove_reader(fd)

    try:
        data, addr = sock.recvfrom(n_bytes)
    except (BlockingIOError, InterruptedError):
        loop.add_reader(fd, sock_recvfrom, loop, sock, n_bytes, fut, True)
    else:
        fut.set_result((data, addr))
    return fut

def sock_sendto(loop, sock, data, addr, fut=None, registed=False):
    """
    CREDITS TO https://pysheeet-kr.readthedocs.io/ko/latest/notes/python-asyncio.html#simple-asyncio-udp-echo-server 
    """
    fd = sock.fileno()
    if fut is None:
        fut = loop.create_future()
    if registed:
        loop.remove_writer(fd)
    if not data:
        return

    try:
        n = sock.sendto(data, addr)
    except (BlockingIOError, InterruptedError):
        loop.add_writer(fd, sock_sendto, loop, sock, data, addr, fut, True)
    else:
        fut.set_result(n)
    return fut

async def listen():
    loop = aio.get_running_loop()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setblocking(False)
        sock.bind(('', PORT))

        while True:
            line, addr = await sock_recvfrom(loop, sock, 1024)
            print('received msg:', line)

async def send(msg, ip):
    loop = aio.get_running_loop()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setblocking(False)
        # sock.bind(('', 0))
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print(f'broadcast {msg=} {ip=}')

        await sock_sendto(loop, sock, b'hello', (ip, PORT))


ips = ["25.88.104.2"]

async def main():

    listen_task = aio.create_task(listen())
    for ip in ips:
        await send('hello', ip)
        await aio.sleep(1)
    await listen_task

aio.run(main())
