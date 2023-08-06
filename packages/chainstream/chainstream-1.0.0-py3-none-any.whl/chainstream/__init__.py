"""
© Reuben Thomas 2023.
This package is distributed under CC-BY-SA 4.0.
See https://creativecommons.org/licenses/by-sa/4.0/

Adapted from: https://stackoverflow.com/questions/24528278
Note: the original code is licensed under CC-BY-SA 3.0, which is
upwards-compatible with 4.0.
"""

from __future__ import annotations

import io
from typing import Optional, IO, List, TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import WriteableBuffer

class ChainStream(io.RawIOBase):
    """
    Chain an iterable of IO[bytes] together into a single buffered stream.
    Usage:
        def generate_open_file_streams():
            for file in filenames:
                yield open(file, 'rb')
        f = io.BufferedReader(ChainStream(generate_open_file_streams()))
        f.read()
    """
    def __init__(self, streams: List[IO[bytes]]):
        super().__init__()
        self.leftover = b''
        self.stream_iter = iter(streams)
        try:
            self.stream: Optional[IO[bytes]] = next(self.stream_iter)
        except StopIteration:
            self.stream = None

    def readable(self) -> bool:
        return True

    def _read_next_chunk(self, max_length: int) -> bytes:
        # Return 0 or more bytes from the current stream, first returning all
        # leftover bytes. If the stream is closed returns b''
        if self.leftover:
            return self.leftover
        if self.stream is not None:
            data = self.stream.read(max_length)
            assert data is not None # FIXME: allow stream to be non-blocking
            return data
        return b''

    def readinto(self, b: WriteableBuffer) -> int:
        mem = memoryview(b) # Allow slicing of the buffer
        buffer_length = len(mem)
        chunk = self._read_next_chunk(buffer_length)
        while len(chunk) == 0:
            # move to next stream
            if self.stream is not None:
                self.stream.close()
            try:
                self.stream = next(self.stream_iter)
                chunk = self._read_next_chunk(buffer_length)
            except StopIteration:
                # No more streams to chain together
                self.stream = None
                return 0  # indicate EOF
        output, self.leftover = chunk[:buffer_length], chunk[buffer_length:]
        mem[:len(output)] = output
        return len(output)
