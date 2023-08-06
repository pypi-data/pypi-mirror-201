import logging
from .basic import (
    BasicFilter,
    ReadableBuffer,
    WritableBuffer,
    ReadRetType,
)

_log = logging.getLogger('kedixa.comm.debug_filter')
__all__ = [
    'DebugFilter',
]


class DebugFilter(BasicFilter):
    def __init__(self, size_limit: int = 128):
        super().__init__()
        self._limit: int = size_limit

    async def write(self, buffer: ReadableBuffer) -> int:
        ret = await self._nxt.write(buffer)
        x = min(ret, self._limit)
        _log.debug('write len:%d data:%s', ret, buffer[:x])
        return ret

    async def read(self, max_bytes: int = -1, *,
            buffer: WritableBuffer = None) -> ReadRetType:
        ret = await self._nxt.read(max_bytes, buffer=buffer)

        if buffer is None:
            buf, rlen = ret, len(ret)
        else:
            buf, rlen = buffer, ret
        x = min(rlen, self._limit)
        _log.debug('read len:%d data:%s', rlen, buf[:x])
        return ret

    async def flush(self):
        ret = await self._nxt.flush()
        _log.debug(f'flush ret:{ret}')
        return ret
