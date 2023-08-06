# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import asyncio

from tempfile import TemporaryFile

from .base import Utils

from ..interface import ContextManager


class _BufferAbstract:

    def __init__(self, maxsize=0):

        self._buffer: asyncio.Queue = asyncio.Queue(maxsize)
        
        self._consume_task: asyncio.Task = Utils.create_task(
            self._do_consume_task()
        )

    async def _do_consume_task(self, data):
        raise NotImplementedError()

    def cancel(self):
        self._consume_task.cancel()

    def qsize(self):

        return self._buffer.qsize()

    def append(self, data):

        self._buffer.put_nowait(data)

    async def append_wait(self, data, timeout=0):

        if timeout > 0:
            await asyncio.wait_for(
                self._buffer.put(data),
                timeout
            )
        else:
            await self._buffer.put(data)


class DataQueue(_BufferAbstract):

    def __init__(self, handler, task_limit=1, maxsize=0):

        super().__init__(maxsize)

        self._handler = handler

        self._tasks = set()

        self._task_limit = task_limit
        self._wait_future: asyncio.Future = None

    async def _do_consume_task(self):

        while True:

            try:

                if len(self._tasks) < self._task_limit:

                    data = await self._buffer.get()

                    task = Utils.create_task(
                        self._handler(data)
                    )

                    task.add_done_callback(self._on_task_done)
                    self._tasks.add(task)

                else:

                    self._wait_future = asyncio.Future()
                    await self._wait_future
                    self._wait_future = None

            except Exception as err:

                Utils.log.error(str(err))

    def _on_task_done(self, task):

        if task in self._tasks:
            self._tasks.remove(task)

        if self._wait_future is not None and self._wait_future.done() is False:
            self._wait_future.set_result()

    def size(self):

        return len(self._tasks)


class QueueBuffer(DataQueue):

    def __init__(self, handler, slice_size, timeout=1, task_limit=1, maxsize=0):

        super().__init__(handler, task_limit, maxsize)

        self._slice_data = []
        self._slice_size = slice_size
        self._timeout = timeout

    async def _get_slice_data(self):

        for _ in range(self._slice_size):
            self._slice_data.append(
                await self._buffer.get()
            )

    async def _do_consume_task(self):

        while True:

            try:

                if len(self._tasks) < self._task_limit:

                    try:
                        await asyncio.wait_for(
                            self._get_slice_data(),
                            self._timeout
                        )
                    except asyncio.TimeoutError:
                        pass

                    if self._slice_data:

                        task = Utils.create_task(
                            self._handler(self._slice_data.copy())
                        )

                        task.add_done_callback(self._on_task_done)
                        self._tasks.add(task)

                        self._slice_data.clear()

                else:

                    self._wait_future = asyncio.Future()
                    await self._wait_future
                    self._wait_future = None

            except Exception as err:

                Utils.log.error(str(err))

    def qsize(self):

        return super().qsize() + len(self._slice_data)


class FileBuffer(ContextManager):
    """文件缓存类
    """

    def __init__(self, slice_size=0x1000000):

        self._buffers = []

        self._slice_size = slice_size

        self._read_offset = 0

        self._append_buffer()

    def _context_release(self):

        self.close()

    def _append_buffer(self):

        self._buffers.append(TemporaryFile())

    def close(self):

        while len(self._buffers) > 0:
            self._buffers.pop(0).close()

        self._read_offset = 0

    def write(self, data):

        buffer = self._buffers[-1]

        buffer.seek(0, 2)
        buffer.write(data)

        if buffer.tell() >= self._slice_size:
            buffer.flush()
            self._append_buffer()

    def read(self, size=None):

        buffer = self._buffers[0]

        buffer.seek(self._read_offset, 0)

        result = buffer.read(size)

        if len(result) == 0 and len(self._buffers) > 1:
            self._buffers.pop(0).close()
            self._read_offset = 0
        else:
            self._read_offset = buffer.tell()

        return result
