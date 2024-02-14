from abc import ABC, abstractmethod


class BaseETLPipeline(ABC):
    @abstractmethod
    def extract(self):
        ...

    @abstractmethod
    def transform(self):
        ...

    @abstractmethod
    def load(self):
        ...

    @abstractmethod
    def get_data(self):
        ...