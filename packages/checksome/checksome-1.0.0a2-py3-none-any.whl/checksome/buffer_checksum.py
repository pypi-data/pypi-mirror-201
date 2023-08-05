from io import BufferedReader
from typing import Optional, Union

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

    def checksum(
        self,
        offset: Optional[int] = None,
        length: Optional[int] = None,
    ) -> bytes:
        """
        Gets the checksum of the buffer.

        If `offset` is set then the checksum will be calculated only for bytes
        from that offset. If `offset` is omitted then the buffer will be read
        from the start.

        If `length` is set then the checksum will be calculated only for that
        given length of bytes. If `length` is omitted then the buffer will be
        read to the end.
        """

        wip = self._algo.new()
        remaining = length

        offset = 0 if offset is None else offset

        self._buffer.seek(offset)

        while remaining is None or remaining > 0:
            if remaining is None:
                read_len = self._chunk_len
            else:
                read_len = min(remaining, self._chunk_len)
                remaining -= read_len

            data = self._buffer.read(read_len)
            end = len(data) < read_len

            if end and length is not None:
                raise UnexpectedEndOfBuffer(offset, length)

            wip.update(data)

            if end:
                break

        return wip.digest()

    def has_checksum(
        self,
        expect: Union[bytes, str],
        offset: Optional[int] = None,
        length: Optional[int] = None,
    ) -> bool:
        """
        Checks if the buffer has the expected checksum.

        `expect` can be the expected checksum as either bytes or a hexadecimal
        string.

        If `offset` is set then the checksum will be calculated only for bytes
        from that offset. If `offset` is omitted then the buffer will be read
        from the start.

        If `length` is set then the checksum will be calculated only for that
        given length of bytes. If `length` is omitted then the buffer will be
        read to the end.
        """

        actual = self.checksum(offset=offset, length=length)

        expect = bytes.fromhex(expect) if isinstance(expect, str) else expect
        log_offset = 0 if offset is None else offset
        log_end = "end" if length is None else log_offset + length

        if actual == expect:
            logger.debug(
                "Bytes %s-%s have expected checksum %s",
                log_offset,
                log_end,
                expect.hex(),
            )

            return True

        logger.debug(
            "Expected checksum %s for bytes %s-%s but discovered %s",
            expect.hex(),
            log_offset,
            log_end,
            actual.hex(),
        )

        return False
