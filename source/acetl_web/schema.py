from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, AliasChoices

data_status_alias = AliasChoices('dataStatus', 'data_status')


class ProductDTO(BaseModel):
    id: UUID
    name: str = Field(validation_alias=AliasChoices('name', "Product Name"))
    code: UUID = Field(validation_alias=AliasChoices('code', 'Product Code'))
    price: Optional[float] = Field(validation_alias=AliasChoices('price', 'Price'))
    quantity: Optional[int] = Field(validation_alias=AliasChoices("quantity", "Quantity"))
    category: Optional[str] = Field(validation_alias=AliasChoices("category", "Category"))
    creation_date: datetime

    class Config:
        """
        from_orm is deprecated,
        use from_attribute=True and model_validate method instead in pydantic v2
        """
        from_attributes = True


class ProductFirstChunkList(BaseModel):
    data: List[ProductDTO]
