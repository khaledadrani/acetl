import pathlib
from typing import Union, Iterable

import pandas as pd

from source.core.base_etl import BaseETLPipeline


class SimpleETLPipeline(BaseETLPipeline): # (optional?) divide by chunk size = 100 default do operation for each chunk
    # no need to use async all the time, use multiprocessing/process pool (map executor) syncrhon since this is data (no concurrency with multiple users)
    # make sure to set a limit size (say 5 mo, so around 20k rows, test the performance)
    # make simple unit tests
    # high priority end2end
    """
    https://www.vinta.com.br/blog/etl-with-asyncio-asyncpg
    https://www.kaggle.com/datasets/sanlian/online-retail-dataset?resource=download
    """
    def __init__(self, data_path: Union[pathlib.Path, Iterable[pathlib.Path]]) -> None:
        """

        :param data_path:
        """
        if isinstance(data_path, pathlib.Path):
            data_path = [data_path]

        self.data_path: Iterable[pathlib.Path] = data_path

        self.current_data = []

    def extract(self):
        self.current_data = [pd.read_csv(path) for path in self.data_path]

    def transform(self):
        ...


