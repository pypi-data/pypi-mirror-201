from abc import ABC, abstractmethod


class Hash(ABC):
    """
    Hash.
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


class Algorithm(ABC):
    """
    Hashing algorithm.
    """

    @abstractmethod
    def new(self) -> Hash:
        """
        Creates and returns a new empty hash.
        """
