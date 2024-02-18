import typer
from loguru import logger
from sqlalchemy import create_engine
import pathlib
from source.configuration.config import DatabaseConfig
from source.core.multiple_files_etl import MultipleFilesETLPipeline
from source.core.simple_etl import SimpleETLPipeline
from source.models.product_model import Base
from opentelemetry import trace
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

db_config = DatabaseConfig()

engine = create_engine(db_config.database_url)

Base.metadata.create_all(engine)

cli_app = typer.Typer()


@cli_app.command()
def etl_single_file(data_path: str):
    data_path = pathlib.Path(data_path)

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
    tracer = trace.get_tracer(__name__)

    trace.set_tracer_provider(TracerProvider())

    # Set up the tracer provider
    trace.set_tracer_provider(TracerProvider())

    # Set up the span exporter
    trace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(ConsoleSpanExporter())
    )

    # Get the tracer
    tracer = trace.get_tracer(__name__)

    # Create a new root span, set it as the current span in context
    with tracer.start_as_current_span("parent"):
        cli_app()
