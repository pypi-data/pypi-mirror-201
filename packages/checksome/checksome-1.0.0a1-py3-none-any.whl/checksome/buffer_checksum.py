from io import BufferedReader

from checksome.algorithms import Algorithm
from checksome.exceptions import UnexpectedEndOfBuffer
from checksome.logging import logger


class BufferChecksum:
    """
    Buffer checksum reader.

    `chunk_len` prescribes the maximum number of bytes to read at a time.
    Defaults to 64 kilobytes.
    """

    def __init__(
        self,
        algorithm: Algorithm,
        buffer: BufferedReader,
        chunk_len: int = 65_536,
    ) -> None:
        self._algo = algorithm
        self._buffer = buffer
        self._chunk_len = chunk_len

    def checksum(self, offset: int, length: int) -> bytes:
        """
        Gets the checksum of the bytes from `offset` for `length`.
        """

        wip = self._algo.new()
        remaining = length

        self._buffer.seek(offset)

        while remaining > 0:
            read_len = min(length, self._chunk_len)
            remaining -= read_len
            data = self._buffer.read(read_len)

            if len(data) < read_len:
                raise UnexpectedEndOfBuffer(offset, length)

            wip.update(data)

        return wip.digest()

    def has_checksum(self, offset: int, length: int, expect: bytes) -> bool:
        """
        Checks if the bytes from `offset` for `length` have the expected
        checksum.
        """

        actual = self.checksum(offset, length)

        if actual == expect:
            logger.debug(
                "Bytes %s-%s have expected checksum %s",
                offset,
                offset + length,
                expect.hex(),
            )

            return True

        logger.debug(
            "Expected checksum %s for bytes %s-%s but discovered %s",
            expect.hex(),
            offset,
            offset + length,
            actual.hex(),
        )

        return False
