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

    def __call__(self, *args, **kwargs):
        self.extract()

        self.transform()

        self.load()
