from abc import ABC, abstractmethod
from typing import Any

from source.common.schema.core_schema import FilePath


# Abstract class with __call__ method
class StringSearchAlgorithm(ABC):

    def __init__(self, directory: FilePath):
        self.directory = directory

    @abstractmethod
    def __call__(self, key: Any):
        raise NotImplementedError
