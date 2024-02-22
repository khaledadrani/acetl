from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from source.acetl_web.inversion_of_control import DependencyContainer
from source.acetl_web.schema import ProductFirstChunkList
from source.acetl_web.service import ProductService
from source.common.configuration.logging_config import logger

data_fetch_router = APIRouter(prefix="/read")


@data_fetch_router.get("/first-chunk", response_model=ProductFirstChunkList)
@inject
def get_first_chunk(
        product_service: ProductService = Depends(Provide[DependencyContainer.product_service])
) -> ProductFirstChunkList:
    """
    Returns the first 10 lines from the Product Table
    :return: ProductFirstChunkList
    """
    logger.info("request!!!")

    return product_service.get_data_overview()
