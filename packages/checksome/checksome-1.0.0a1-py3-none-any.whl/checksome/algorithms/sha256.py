from hashlib import sha256

from checksome.algorithms.base import Algorithm, Hash


class SHA256Hash(Hash):
    """
    SHA256 hash.
    """

    def __init__(self) -> None:
        self.sha256 = sha256(usedforsecurity=False)

    def digest(self) -> bytes:
        """
        Gets the hash digest.
        """

        return self.sha256.digest()

    def update(self, data: bytes) -> None:
        """
        Adds bytes to the hash.
        """

        self.sha256.update(data)


class SHA256(Algorithm):
    """
    SHA245 hashing algorithm.
    """

    def new(self) -> SHA256Hash:
        """
        Creates and returns a new empty SHA256 hash.
        """

        return SHA256Hash()
