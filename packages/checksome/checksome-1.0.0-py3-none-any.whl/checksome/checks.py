from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Type, Union

from checksome.algorithms import Algorithm
from checksome.reader import ChecksumReader


def checksum(
    path: Union[Path, str],
    algorithm: Type[Algorithm],
    offset: Optional[int] = None,
    length: Optional[int] = None,
) -> bytes:
    """
    Gets the checksum of a file's content.

    If `offset` is set then the checksum will be calculated only for bytes
    from that offset. If `offset` is omitted then the buffer will be read
    from the start.

    If `length` is set then the checksum will be calculated only for that
    given length of bytes. If `length` is omitted then the buffer will be
    read to the end.
    """

    with checksum_reader(path, algorithm) as f:
        return f.checksum(offset=offset, length=length)


@contextmanager
def checksum_reader(
    path: Union[Path, str],
    algorithm: Type[Algorithm],
) -> Iterator[ChecksumReader]:
    """
    Creates and returns a `ChecksumReader` for a file.

    This should be used as a context manager to ensure the file is properly
    closed. For example:

    ```python
    with checksum_reader("clowns.jpg", SHA256) as file:
        file.checksum(...)
    ```
    """

    with open(path, "rb") as f:
        yield ChecksumReader(algorithm, f)


def has_checksum(
    path: Union[Path, str],
    algorithm: Type[Algorithm],
    expect: Union[bytes, str],
    offset: Optional[int] = None,
    length: Optional[int] = None,
) -> bool:
    """
    Checks if a file has the expected checksum.

    `expect` can be the expected checksum as either bytes or a hexadecimal
    string.

    If `offset` is set then the checksum will be calculated only for bytes from
    that offset. If `offset` is omitted then the file will be read from the
    start.

    If `length` is set then the checksum will be calculated only for that given
    length of bytes. If `length` is omitted then the file will be read to the
    end.
    """

    with checksum_reader(path, algorithm) as f:
        return f.has_checksum(expect, offset=offset, length=length)
