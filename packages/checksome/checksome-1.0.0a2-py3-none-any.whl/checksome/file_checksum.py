from io import BufferedReader
from pathlib import Path
from typing import Optional, Type, Union

from checksome.algorithms import Algorithm
from checksome.buffer_checksum import BufferChecksum


class FileChecksum:
    """
    File checksum context manager.
    """

    def __init__(self, path: Union[Path, str], algorithm: Algorithm) -> None:
        self._algorithm = algorithm
        self._buffer: Optional[BufferedReader] = None
        self._path = path
        self._reader: Optional[BufferChecksum] = None

    def __enter__(self) -> "BufferChecksum":
        self._buffer = open(self._path, "rb")
        self._reader = BufferChecksum(self._algorithm, self._buffer)
        return self._reader

    def __exit__(
        self,
        ex_type: Optional[Type[Exception]],
        ex: Optional[Exception],
        ex_traceback: Optional[str],
    ) -> bool:
        if self._buffer is not None and not self._buffer.closed:
            self._buffer.close()

        return ex_type is None
