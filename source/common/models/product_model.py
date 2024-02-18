import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Double, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as SqlAlchemyUUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    ...


class ProductModel(Base):
    __tablename__ = 'product'

    id: Mapped[uuid.UUID] = mapped_column(SqlAlchemyUUID(as_uuid=True),
                                          primary_key=True,
                                          default=uuid.uuid4,
                                          unique=True)

    name: Mapped[str] = mapped_column(String, nullable=True, name="Product Name")
    code: Mapped[str] = mapped_column(SqlAlchemyUUID, nullable=True, name="Product Code")
    price: Mapped[float] = mapped_column(Double, nullable=True, name="Price")
    quantity: Mapped[int] = mapped_column(Integer, nullable=True, name="Quantity")
    category: Mapped[str] = mapped_column(String, nullable=True, name="Category")
    creation_date: Mapped[datetime] = mapped_column(DateTime,
                                                    default=datetime.now(timezone.utc),
                                                    server_default=func.now(),
                                                    nullable=False)
