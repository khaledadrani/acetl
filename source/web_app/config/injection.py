from dependency_injector import containers, providers

from source.common.configuration.config import DatabaseConfig
from source.common.gateways.database_helper import Database
from source.web_app.repositories.csv_repository import ProductRepository
from source.web_app.services.csv_demo_service import ProductService


class DependencyContainer(containers.DeclarativeContainer):
    """Container class for dependency injection"""
    wiring_config = containers.WiringConfiguration(packages=["source"])
    db_config = providers.Singleton(DatabaseConfig)

    database_helper = providers.Singleton(Database)

    product_service = providers.Factory(ProductService,
                                        product_repository_type=ProductRepository,
                                        database_config=db_config)
