import concurrent.futures
import pathlib
from typing import List

from loguru import logger

from source.etl_acetl.simple_etl import SimpleETLPipeline
from source.common.configuration.config import DatabaseConfig


def call_etl_for_a_single_file(data_path: str):
    etl = SimpleETLPipeline(data_path=pathlib.Path(data_path),
                            database_url=DatabaseConfig().database_url
                            )

    etl()


class MultipleFilesETLPipeline:
    def __init__(self, data_list: List[str]):
        self.data_list: List[str] = data_list

    def __call__(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Use the map method to execute functions concurrently
            results = list(executor.map(call_etl_for_a_single_file, self.data_list, timeout=60, chunksize=1))

        logger.info(f"Processed files count {len(results)}")
