import uuid
from decimal import Decimal

from pydantic import BaseModel, Field

MIN_QUANTITY = 1


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(ge=MIN_QUANTITY)


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal

    class Config:
        from_attributes = True
