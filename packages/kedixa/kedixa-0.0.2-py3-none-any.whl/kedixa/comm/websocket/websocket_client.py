import asyncio
import random
import base64
import hashlib
import ssl
from urllib.parse import urlparse
from typing import (
    List,
    Tuple,
    Callable,
    Awaitable,
)

from .. import (
    Connection,
    TcpAdaptor,
    SslFilter,
    ReadUntilFilter,

    getaddrinfo,
)
from ..http import (
    HttpRequest,
    HttpResponse,
)
from .websocket_message import (
    WebSocketFrame,
    WebSocketOpcode,
)

__all__ = [
    'SEC_WS_APPEND',
    'get_sec_ws_accept',
    'get_sec_ws_pair',
    'WebSocketClient',
]

SEC_WS_APPEND = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

def get_sec_ws_accept(key: str) -> str:
    accept = key + SEC_WS_APPEND
    accept = hashlib.sha1(accept.encode()).digest()
    accept = base64.b64encode(accept).decode()
    return accept

def get_sec_ws_pair() -> Tuple[str, str]:
    key = bytes(random.choices(range(0, 256), k=16))
    key: str = base64.b64encode(key).decode()
    return key, get_sec_ws_accept(key)

def _ws_parse_url(url: str):
    u = urlparse(url)
    scheme = u.scheme.lower()
    assert scheme in ['ws', 'wss']

    host, port = u.hostname, u.port
    assert host is not None

    if port is None:
        if scheme == 'wss':
            port = 443
        else:
            port = 80

    req_url: str = '/' if len(u.path) == 0 else u.path
    if len(u.query) > 0:
        req_url += '?' + u.query

    return scheme, host, port, req_url

WsTextHandlerType = Callable[['WebSocketClient', str], Awaitable[None]]
WsBinaryHandlerType = Callable[['WebSocketClient', bytes], Awaitable[None]]
WsFramesHandlerType = Callable[['WebSocketClient', List[WebSocketFrame]], Awaitable[None]]

class WebSocketClient:
    def __init__(self, url: str, *,
            ssl_ctx: ssl.SSLContext = None,
            upgrade_headers: List[Tuple[str, str]] = None,
            on_text: WsTextHandlerType = None,
            on_binary: WsBinaryHandlerType = None,
            on_frames: WsFramesHandlerType = None,
            ):
        self._url : str = url
        self._ssl_ctx: ssl.SSLContext = ssl_ctx
        self._on_text: WsTextHandlerType = on_text
        self._on_binary: WsBinaryHandlerType = on_binary
        self._on_frames: WsFramesHandlerType = on_frames

        self._conn: Connection = None
        self._closed: bool = True
        self._recv_task: asyncio.Task = None
        self._context = None

        self._ex_hdrs: List[Tuple[str, str]] = \
            upgrade_headers if upgrade_headers is not None else []

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    def closed(self) -> bool:
        return self._closed

    async def _receive_msgs(self) -> List[WebSocketFrame]:
        msgs = []
        while True:
            msg = WebSocketFrame()
            await self._conn.request(None, msg)
            msgs.append(msg)
            if msg.fin:
                break

        return msgs

    async def _handle_msg(self, msgs: List[WebSocketFrame]):
        opcode = msgs[0].opcode
        if opcode == WebSocketOpcode.TextFrame and self._on_text:
            data = bytes().join([m.payload for m in msgs])
            try:
                data = data.decode()
            except UnicodeDecodeError:
                pass
            await self._on_text(self, data)
        elif opcode == WebSocketOpcode.BinaryFrame and self._on_binary:
            data = bytes().join([m.payload for m in msgs])
            await self._on_binary(self, data)
        elif self._on_frames:
            await self._on_frames(self, msgs)
        else:
            pass

    async def _process_msg(self):
        try:
            while not self.closed():
                msgs = await self._receive_msgs()
                if len(msgs) == 0:
                    continue

                await self._handle_msg(msgs)
        except asyncio.CancelledError:
            return

    async def _open(self):
        scheme, host, port, req_url = _ws_parse_url(self._url)
        addrs = await getaddrinfo(host, port)

        # TODO assert(len(addrs) > 0)
        self._conn = Connection(TcpAdaptor(addrs[0]))

        try:
            await self._conn.open()

            if scheme == 'wss':
                if self._ssl_ctx is None:
                    self._ssl_ctx = ssl.create_default_context()
                s = SslFilter(self._ssl_ctx, host)
                await self._conn.bind(s)

            await self._conn.bind(ReadUntilFilter())

            sec_key, sec_accept = get_sec_ws_pair()
            http_req = HttpRequest(req_url=req_url)
            http_resp = HttpResponse()

            for exhdr in self._ex_hdrs:
                http_req.set_header(exhdr[0], exhdr[1])

            http_req.set_header('Host', host, overwrite=False)
            http_req.set_header('Connection', 'Upgrade')
            http_req.set_header('Upgrade', 'websocket')
            http_req.set_header('Sec-WebSocket-Version', '13')
            http_req.set_header('Sec-WebSocket-Key', sec_key)


            await self._conn.request(http_req, http_resp)
            if http_resp.get_status_code() != 101:
                print(http_resp)
                raise Exception('TODO upgrade failed')

            resp_accept = http_resp.get_header('Sec-WebSocket-Accept')
            if len(resp_accept) != 1 or sec_accept != resp_accept[0]:
                raise Exception('TODO upgrade failed')

            proc = self._process_msg()
            self._recv_task = asyncio.ensure_future(proc)
        except:
            self._recv_task = None
            await self._conn.close()
            self._conn = None
            raise

    async def __aenter__(self):
        await self.open()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def open(self):
        if self._closed:
            await self._open()
            self._closed = False

    async def close(self):
        if not self._closed:
            self._closed = True

            try:
                self._recv_task.cancel()
                await self._conn.close()
            finally:
                self._conn = None
                self._recv_task = None

    async def send(self, type: int, data: bytes):
        mask = random.randint(0, 2**32-1)
        msg = WebSocketFrame(opcode=type, mask=mask, payload=data)
        async with self._conn.lock:
            await self._conn.request(msg, None)

    async def send_text(self, text: str):
        await self.send(WebSocketOpcode.TextFrame, text.encode())

    async def send_binary(self, data: bytes):
        await self.send(WebSocketOpcode.BinaryFrame, data)

    async def send_ping(self):
        await self.send(WebSocketOpcode.Ping, bytes())

    async def send_pong(self):
        await self.send(WebSocketOpcode.Pong, bytes())