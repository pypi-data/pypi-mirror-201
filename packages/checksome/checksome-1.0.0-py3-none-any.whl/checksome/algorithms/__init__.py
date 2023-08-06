from typing import Dict, Type

from checksome.algorithms.algorithm import Algorithm
from checksome.algorithms.sha256 import SHA256


def get_algorithm(name: str) -> Type[Algorithm]:
    """
    Gets the hashing algorithm of the given name.
    """

    algorithms: Dict[str, Type[Algorithm]] = {
        "sha256": SHA256,
    }

    a_cls = algorithms.get(name.lower())

    if a_cls is not None:
        return a_cls

    raise ValueError(f'No algorithm named "{name}"')


__all__ = [
    "Algorithm",
    "SHA256",
]
