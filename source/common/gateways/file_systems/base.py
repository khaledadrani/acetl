import pathlib
from abc import ABC, abstractmethod
import os
from typing import Generator


class FileSystemInterface(ABC):
    @abstractmethod
    def store(self, key, data):
        raise NotImplementedError()

    @abstractmethod
    def get(self, key):
        raise NotImplementedError()

    @abstractmethod
    def get_list(self):
        raise NotImplementedError()


class LocalFileSystem(FileSystemInterface):
    def __init__(self, directory: str):
        self.directory: pathlib.Path = pathlib.Path(directory)

    def store(self, key, data, mode: str = 'w'):
        file_path = self.directory / pathlib.Path(key)
        with open(file_path, mode) as file:
            file.write(data)

    def get(self, key, mode: str = 'rb'):
        file_path = self.directory / pathlib.Path(key)
        try:
            with open(str(file_path), mode) as file:
                return file.read()
        except FileNotFoundError:
            return None

    def get_list(self, pattern: str = '*', is_recursive: bool = False) -> Generator[str, None, None]:
        search = self.directory.rglob if is_recursive else self.directory.glob

        for path in search(pattern):
            yield path
