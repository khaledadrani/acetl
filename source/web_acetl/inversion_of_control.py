from dependency_injector import containers, providers

from source.acetl_web.database_helper import Database
from source.acetl_web.repository import ProductRepository
from source.acetl_web.service import ProductService
from source.common.configuration.config import DatabaseConfig


class DependencyContainer(containers.DeclarativeContainer):
    """Container class for dependency injection"""
    wiring_config = containers.WiringConfiguration(packages=["source"])
    db_config = providers.Singleton(DatabaseConfig)

    database_helper = providers.Singleton(Database)

    product_service = providers.Factory(ProductService,
                                        product_repository_type=ProductRepository,
                                        database_config=db_config)
