from typing import Iterable, List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from source.acetl_web.schema import ProductDTO
from source.common.configuration.config import DatabaseConfig
from source.common.models.product_model import ProductModel


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_first_chunk(self, limit_value: int = 10) -> List[ProductDTO]:
        result = (self.session.query(ProductModel)
                  # .order_by(desc(ProductModel.creation_date))
                  .limit(limit_value))

        return [ProductDTO.model_validate(row) for row in result.all()]
