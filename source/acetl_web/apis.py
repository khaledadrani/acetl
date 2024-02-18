from fastapi import APIRouter

from source.acetl_web.database_helper import Database
from source.acetl_web.repository import ProductRepository
from source.acetl_web.schema import ProductFirstChunkList
from source.common.configuration.config import DatabaseConfig

data_fetch_router = APIRouter(prefix="/read")


@data_fetch_router.get("/first-chunk", response_model=ProductFirstChunkList)
def get_first_chunk() -> ProductFirstChunkList:
    """
    •Description: Returns the first 10 lines from Database
    •Request: Get /read/first-chunck
    •Response: 200 OK
    •Response Body: JSON
    •Response Body Description: A list of 10 JSON objects
    :return:
    """

    db_helper = Database(DatabaseConfig().database_url)

    with db_helper.session() as session:
        repository = ProductRepository(session=session)

        return ProductFirstChunkList(data=repository.get_first_chunk())
