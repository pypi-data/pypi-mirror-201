from pathlib import Path
from typing import Union

from checksome.algorithms import Algorithm
from checksome.file_checksum import FileChecksum


def checksum_file(
    path: Union[Path, str],
    algorithm: Algorithm,
) -> FileChecksum:
    """
    Creates and returns a checksum reader for a file.

    This should be used as a context manager to ensure the file is properly
    closed. For example:

    ```python
    with checksum_file("clowns.jpg", SHA256()) as file:
        file.checksum(...)
    ```
    """
    return FileChecksum(path, algorithm)
