import pathlib
import uuid
from typing import Optional

import pandas as pd
import profilehooks
from sqlalchemy import create_engine, Integer, Double, String
from sqlalchemy.orm import Session

from source.acetl_etl.base_etl import BaseETLPipeline
from source.common.configuration.logging_config import logger
from source.common.configuration.tracing import trace_process
from source.common.models.product_model import ProductModel, SqlAlchemyUUID


def parse_valid_uuid(value):
    try:
        uuid.UUID(value)
        return value
    except (ValueError, AttributeError):
        return None


class SimpleETLPipeline(BaseETLPipeline):
    # (optional?) divide by chunk size = 100 default do operation for each chunk
    # no need to use async all the time, use multiprocessing/process pool (map executor) syncrhon since this is data (no concurrency with multiple users)
    # make sure to set a limit size (say 5 mo, so around 20k rows, test the performance)
    # make simple unit tests
    # high priority end2end

    # execute with one FILE!
    """
    https://www.vinta.com.br/blog/etl-with-asyncio-asyncpg
    https://www.kaggle.com/datasets/sanlian/online-retail-dataset?resource=download
    https://stackoverflow.com/questions/42074501/python-concurrent-futures-processpoolexecutor-performance-of-submit-vs-map
    """

    step_order = ["EXTRACT", "TRANSFORM", "LOAD"]  # TODO to check order of execution

    def __init__(self, data_path: pathlib.Path, database_url: str, chunk_size: int = 1000) -> None:
        """

        :param data_path:
        """

        self.data_path: pathlib.Path = data_path
        self.chunk_size = chunk_size

        self.current_data: Optional[pd.DataFrame] = None
        self.data_name: str = self.data_path.stem
        self.database_url: str = database_url

        self.current_step: int = -1  # TODO use this to check for the correct step each time

    def _log_data_info(self, process_name: Optional[str] = None):
        if process_name:
            logger.info(f"{self.data_name}  After {process_name}")

        logger.info(f"{self.data_name} Data Size {len(self.current_data)}")

        logger.info(f"{self.data_name} NA values \n{self.current_data.isna().sum()}")

    def get_data(self) -> pd.DataFrame:
        return self.current_data

    def extract(self) -> None:
        # TODO  read data lazily by chunk, to avoid loading it entirely in memory

        self.current_data = pd.read_csv(self.data_path)
        self._log_data_info('EXTRACT')

    def transform(self) -> None:
        # assume we are going to drop items with no product code or product name
        self.current_data[ProductModel.code.name] = self.current_data[ProductModel.code.name].apply(parse_valid_uuid)
        self.current_data = self.current_data.dropna(subset=[ProductModel.code.name, ProductModel.name.name])

        self._log_data_info(process_name="TRANSFORM Product ID, Product Name")
        # assume that we are going to fill missing category cells with the last non na value
        self.current_data[ProductModel.category.name] = self.current_data[ProductModel.category.name].ffill()
        self._log_data_info(process_name="TRANSFORM Category")

        # assume we will force Price and Quantity columns to be numeric,
        self.current_data[ProductModel.price.name] = pd.to_numeric(self.current_data[ProductModel.price.name],
                                                                   errors='coerce')
        self.current_data[ProductModel.quantity.name] = pd.to_numeric(self.current_data[ProductModel.quantity.name],
                                                                      errors='coerce')
        self._log_data_info(process_name="TRANSFORM PRICE")

    def load(self) -> None:
        # add creation_date columns

        engine = create_engine(self.database_url)

        self.current_data[ProductModel.id.name] = [uuid.uuid4() for _ in range(len(self.current_data))]
        self.current_data.to_sql('product', engine, if_exists='append', index=False,
                                 dtype={"id": SqlAlchemyUUID,
                                        "Product Code": SqlAlchemyUUID,
                                        "Quantity": Integer,
                                        "Price": Double,
                                        "Category": String,
                                        },
                                 chunksize=self.chunk_size
                                 )

        with Session(engine) as session:
            result = session.query(ProductModel).count()

        logger.warning(f"New length of the 'products' table:  {result}")

    @profilehooks.timecall(immediate=True)
    def __call__(self):
        # will run  the entire pipeline for a single csv file
        logger.info(f"START ETL {self.data_name}")

        trace_process(self.extract, f"{self.data_name}|{self.step_order[0]}")

        trace_process(self.transform, f"{self.data_name}|{self.step_order[1]}")

        trace_process(self.load, f"{self.data_name}|{self.step_order[2]}")

        logger.info(f"DONE ETL {self.data_name}")
