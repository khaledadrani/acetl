from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, AliasChoices, ConfigDict

data_status_alias = AliasChoices('dataStatus', 'data_status')


class ProductDTO(BaseModel):
    id: UUID
    name: str = Field(validation_alias=AliasChoices('name', "Product Name"))
    code: UUID = Field(validation_alias=AliasChoices('code', 'Product Code'))
    price: Optional[float] = Field(validation_alias=AliasChoices('price', 'Price'))
    quantity: Optional[int] = Field(validation_alias=AliasChoices("quantity", "Quantity"))
    category: Optional[str] = Field(validation_alias=AliasChoices("category", "Category"))
    creation_date: datetime

    model_config = ConfigDict(extra='ignore', from_attributes=True)


class ProductFirstChunkList(BaseModel):
    data: List[ProductDTO]
