from abc import ABC, abstractmethod


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
