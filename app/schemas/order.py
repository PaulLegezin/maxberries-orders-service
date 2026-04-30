import uuid
from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field

from app.schemas.order_items import OrderItemCreate, OrderItemResponse

MIN_PRICE = 0.00


class OrderBase(BaseModel):
    items: list[OrderItemCreate]
    delivery_price: Decimal = Field(default=Decimal("0.00"), ge=0)


class OrderCreate(OrderBase):
    pass


class OrderResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    items: List[OrderItemResponse]
    total_price: Decimal = Field(ge=MIN_PRICE)
    cart_price: Decimal = Field(ge=MIN_PRICE)
    delivery_price: Decimal = Field(ge=MIN_PRICE)
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
