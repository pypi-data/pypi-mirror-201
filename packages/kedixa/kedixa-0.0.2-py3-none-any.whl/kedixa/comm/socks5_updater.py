import struct
import socket
import enum

from typing import List

from .basic import BasicTransformer, MessageBase, CommunicateBase

__all__ = [
    'Socks5Method',
    'Socks5Cmd',
    'Socks5Atype',
    'Socks5HandshakeReq',
    'Socks5HandshakeResp',
    'Socks5AuthReq',
    'Socks5AuthResp',
    'Socks5CmdReq',
    'Socks5CmdResp',
    'Socks5Transformer',
]

class Socks5Method(enum.IntEnum):
    NO_AUTH   = 0
    GSSAPI    = 1
    USER_PASS = 2


class Socks5Cmd(enum.IntEnum):
    CONNECT = 1
    BIND    = 2
    UDP     = 3


class Socks5Atype(enum.IntEnum):
    IPv4     = 1
    HOSTNAME = 2
    IPv6     = 3


class Socks5HandshakeReq(MessageBase):
    def __init__(self, methods: List[int]):
        self._version = 5
        self.methods = methods

    @property
    def methods(self) -> List[int]:
        return self._methods

    @methods.setter
    def methods(self, methods: List[int]):
        assert all([0 <= m <= 255 for m in methods])
        assert 0 < len(methods) <= 255
        self._methods = methods

    async def encode(self, c: CommunicateBase):
        data = bytes([self._version, len(self.methods)] + self.methods)
        await c.write_all(data)


class Socks5HandshakeResp(MessageBase):
    def __init__(self):
        self._version: int = 0
        self._method: int = 0

    @property
    def version(self) -> int:
        return self._version

    @property
    def method(self) -> int:
        return self._method

    async def decode(self, c: CommunicateBase):
        data = await c.read_exactly(2)
        self._version, self._method = struct.unpack('>BB', data)


class Socks5AuthReq(MessageBase):
    def __init__(self, user: bytes, passwd: bytes):
        if isinstance(user, str):
            user = user.encode()
        if isinstance(passwd, str):
            passwd = passwd.encode()

        self._user = user
        self._passwd = passwd

    async def encode(self, c: CommunicateBase):
        data = bytes([0x01, len(self._user)])
        data += self._user
        data += bytes([len(self._passwd)])
        data += self._passwd
        await c.write_all(data)


class Socks5AuthResp(MessageBase):
    def __init__(self):
        self._version: int = 0
        self._status: int = 0

    @property
    def version(self) -> int:
        return self._version

    @property
    def status(self) -> int:
        return self._status

    async def decode(self, c: CommunicateBase):
        data = await c.read_exactly(2)
        self._version, self._status = struct.unpack('>BB', data)


class Socks5CmdReq(MessageBase):
    def __init__(self, cmd: Socks5Cmd, atyp: Socks5Atype, addr: str, port: int):
        self._cmd: Socks5Cmd    = cmd
        self._atyp: Socks5Atype = atyp
        self._addr: str         = addr
        self._port: int         = port

    async def encode(self, c: CommunicateBase):
        data = bytes([5, self._cmd, 0, self._atyp])
        if self._atyp == Socks5Atype.IPv4:
            data += socket.inet_pton(socket.AF_INET, self._addr)
        else:
            raise NotImplementedError(f'Socks5Atype.{self._atyp}')
        data += struct.pack('>H', self._port)
        await c.write_all(data)


class Socks5CmdResp(MessageBase):
    def __init__(self):
        pass

    @property
    def status(self) -> int:
        return self._status

    async def decode(self, c: CommunicateBase):
        data = await c.read_exactly(4)
        ver, rep, rsv, atyp = struct.unpack('>BBBB', data)
        self._status: int = rep
        self._atyp: Socks5Atype = atyp

        if atyp == Socks5Atype.IPv4:
            addr = await c.read_exactly(4)
            self._addr = socket.inet_ntop(socket.AF_INET, addr)
        else:
            raise NotImplementedError(f'Socks5Atype.{atyp}')

        self._port = struct.unpack('>H', await c.read_exactly(2))


class Socks5Updater(BasicTransformer):
    def __init__(self, ip, port, username=None, password=None):
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password

    async def prepare(self):
        methods = [Socks5Method.NO_AUTH, Socks5Method.USER_PASS]
        hsk_req = Socks5HandshakeReq(methods)
        hsk_resp = Socks5HandshakeResp()

        await hsk_req.encode(self)
        await hsk_resp.decode(self)
        method = hsk_resp.method

        if method == Socks5Method.NO_AUTH:
            pass
        elif method == Socks5Method.USER_PASS:
            if self._username is None or self._password is None:
                raise Exception('TODO bad username or password')

            auth_req = Socks5AuthReq(self._username, self._password)
            auth_resp = Socks5AuthResp()
            await auth_req.encode(self)
            await auth_resp.decode(self)
            status = auth_resp.status

            if status != 0:
                raise Exception(f'TODO Socks5 prepare status:{status}')
        else:
            raise Exception(f'TODO Socks5 prepare method:{method}')

        cmd_req = Socks5CmdReq(Socks5Cmd.CONNECT, Socks5Atype.IPv4, self._ip, self._port)
        cmd_resp = Socks5CmdResp()
        await cmd_req.encode(self)
        await cmd_resp.decode(self)
        status = cmd_resp.status

        if status != 0:
            raise Exception(f'TODO Socks5 cmd status:{status}')

