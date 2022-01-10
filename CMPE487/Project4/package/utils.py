import asyncio as aio
import socket

def chunker(seq, size):
    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]

def argmin(sequence, fn=None):
    """Two usage patterns:
    argmin([s0, s1, ...], fn)
    argmin([(fn(s0), s0), (fn(s1, s1), ...]) 
    Both return the si with lowest fn(si)"""
    if fn is None:
        return min(sequence)[1]
    else:
        return min((fn(e), e) for e in sequence)[1]

async def send_udp_packet(addr, packet, timeout=1):
    loop = aio.get_running_loop()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setblocking(False)
        #sock.bind(('', 0))  # <-- from lecture
        await sock_sendto(loop, sock, packet, addr)

async def send_broadcast_udp_packet(addr, packet, timeout=1):
    loop = aio.get_running_loop()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setblocking(False)
        #sock.bind(('', 0))  # <-- from lecture
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        await sock_sendto(loop, sock, packet, addr)


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
