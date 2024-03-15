from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from source.web_app.config.injection import DependencyContainer
from source.web_app.schema.csv_demo_schema import ProductFirstChunkList
from source.web_app.services.csv_demo_service import ProductService

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

    return product_service.get_data_overview()
