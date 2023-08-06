from abc import ABC, abstractmethod


class Algorithm(ABC):
    """
    Abstract implementation of a hashing algorithm.
    """

    @abstractmethod
    def digest(self) -> bytes:
        """
        Gets the hash digest.
        """

    @abstractmethod
    def update(self, data: bytes) -> None:
        """
        Adds bytes to the hash.
        """
