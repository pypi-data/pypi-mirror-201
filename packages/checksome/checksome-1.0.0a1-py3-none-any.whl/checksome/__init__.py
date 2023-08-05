from importlib.resources import open_text

from checksome.algorithms import SHA256
from checksome.checksum import checksum_file

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "SHA256",
    "checksum_file",
]
