import async_timeout
from asyncio import Lock, Queue
from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncContextManager, Any, Dict, List, Optional

import aioredis

from cenao.app import AppFeature


class TeeChannel:
    _tee: 'Tee'
    _queue: Queue

    def __init__(self, tee: 'Tee'):
        self._tee = tee
        self._queue = Queue()

    async def get(self) -> Any:
        if self._queue.empty() and not self._tee.lock.locked():
            async with self._tee.lock:
                await self._tee.get()

        return await self._queue.get()

    async def get_timeout(self, timeout: float):
        async with async_timeout.timeout(timeout):
            return await self.get()

    def put(self, item):
        self._queue.put_nowait(item)

    async def __anext__(self) -> Any:
        return await self.get()


class Tee:
    redis: aioredis.Redis
    channel: str
    lock: Lock = Lock()
    _channel: Optional[aioredis.Channel]
    _channels: List[TeeChannel] = []

    def __init__(self, redis: aioredis.Redis, channel: str):
        self.redis = redis
        self.channel = channel

    async def get(self):
        if not self._channel:
            raise RuntimeError('Must initialize channel first')

        item = await self._channel.get()
        for ch in self._channels:
            ch.put(item)

    async def _start(self):
        channels = await self.redis.subscribe(self.channel)
        self._channel = channels[0]

    async def _stop(self):
        try:
            await self.redis.unsubscribe(self.channel)
        except Exception:
            pass
        finally:
            self._channel = None

    @asynccontextmanager
    async def get_channel(self) -> AsyncGenerator[TeeChannel, None]:
        if self.empty():
            await self._start()

        tee_channel = TeeChannel(self)
        self._channels.append(tee_channel)

        try:
            yield tee_channel
        finally:
            self._channels.remove(tee_channel)
            if self.empty():
                await self._stop()

    def empty(self) -> bool:
        return len(self._channels) == 0


class TeeKeeper:
    redis: aioredis.Redis
    _tees: Dict[str, Tee] = {}

    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    @asynccontextmanager
    async def get_tee_channel(self, channel: str) -> AsyncGenerator[TeeChannel, None]:
        if channel not in self._tees:
            self._tees[channel] = Tee(self.redis, channel)
        tee = self._tees[channel]

        try:
            async with tee.get_channel() as tee_channel:
                yield tee_channel
        finally:
            if tee.empty():
                del self._tees[channel]


class RedisAppFeature(AppFeature):
    """
    Cenao feature for Redis support.
    By default tries connect to `redis://172.17.0.1`, which can be changed via `nodes` config parameter.
    """
    NAME = 'redis'

    _client: aioredis.Redis
    _tee_keeper: Optional[TeeKeeper] = None

    async def on_startup(self):
        cluster = self.config.get('cluster', False)
        nodes = self.config.get('nodes', 'redis://172.17.0.1').split(',')

        if cluster:
            raise NotImplementedError('aioredis-cluster support not implemented yet')
        else:
            self._client = await aioredis.create_redis_pool(nodes[0])

        await self._client.ping()

    async def on_shutdown(self):
        if self._client:
            self._client.close()
            await self._client.wait_closed()

    async def check_health(self) -> bool:
        await self._client.ping()
        return True

    @property
    def client(self):
        """
        Redis instance getter
        :return: A Redis client instance
        """
        return self._client

    def subscribe(self, channel: str) -> AsyncContextManager[TeeChannel]:
        """
        Subscribe (and reuse existing connection) to Redis pubsub channel
        :return: A Tee channel handler
        """
        if not self._client:
            raise RuntimeError('Redis connection must be established first')

        if not self._tee_keeper:
            self._tee_keeper = TeeKeeper(self.client)

        return self._tee_keeper.get_tee_channel(channel)
