import pathlib

import typer
from loguru import logger

from source.etl_csv.multiple_files_etl import MultipleFilesETLPipeline
from source.etl_csv.simple_etl import SimpleETLPipeline
from source.common.configuration.config import DatabaseConfig, ROOT_DIRECTORY
from source.common.utils.generate_dummy_data import save_to_csv, generate_fake_data
from source.common.utils.init_db import initialize_database

initialize_database()

cli_app = typer.Typer()


@cli_app.command()
def generate_dummy_data():
    save_to_csv(generate_fake_data(100), str(ROOT_DIRECTORY/'data/retail_data_small.csv'))
    save_to_csv(generate_fake_data(10000), str(ROOT_DIRECTORY/'data/retail_data_medium.csv'))
    save_to_csv(generate_fake_data(1000000), str(ROOT_DIRECTORY/'data/retail_data_large.csv'))

    print("CSV files generated successfully.")


@cli_app.command()
def etl_single_file(data_path: str):
    data_path = pathlib.Path(data_path)
    db_config = DatabaseConfig()

    if not data_path.exists():
        logger.error(f"{data_path.stem} does not exist!")
        return
    etl = SimpleETLPipeline(data_path, database_url=db_config.database_url)

    etl()


@cli_app.command()
def etl_multiple_files(data_directory: str):
    data_directory = pathlib.Path(data_directory)

    data_list = [str(data_path) for data_path in data_directory.rglob("*.csv") if data_path.exists()]

    if not data_list:
        logger.error(f"{data_directory.stem} is empty!")
        return

    multi_file_etl = MultipleFilesETLPipeline(data_list)

    multi_file_etl()


if __name__ == "__main__":
    cli_app()
