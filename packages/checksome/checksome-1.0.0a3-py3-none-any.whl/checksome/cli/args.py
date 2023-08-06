from dataclasses import dataclass
from pathlib import Path
from typing import Type, Union

from checksome.algorithms import Algorithm


@dataclass
class TaskArgs:
    algorithm: Type[Algorithm]
    source: Union[Path, str]
