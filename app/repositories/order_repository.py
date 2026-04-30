import uuid
from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.internal_client import get_product_price
from app.models.order_items import OrderItem
from app.models.orders import Order
from app.schemas.order import OrderCreate


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, user_id: uuid.UUID, order_data: OrderCreate) -> Order:
        try:
            calculated_cart_price = 0
            order_items_to_add = []

            for item in order_data.items:
                actual_unit_price = await get_product_price(item.product_id)

                calculated_cart_price += actual_unit_price * item.quantity

                order_items_to_add.append(
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "unit_price": actual_unit_price,
                    }
                )

            total_price = calculated_cart_price + order_data.delivery_price

            new_order = Order(
                user_id=user_id,
                total_price=total_price,
                cart_price=calculated_cart_price,
                delivery_price=order_data.delivery_price,
                status="pending",
            )
            self.session.add(new_order)
            await self.session.flush()

            for item_data in order_items_to_add:
                order_item = OrderItem(order_id=new_order.id, **item_data)
                self.session.add(order_item)

            await self.session.commit()
            return await self.get_order_by_id(new_order.id)

        except Exception:
            await self.session.rollback()
            raise

    async def get_order_by_id(self, order_id: uuid.UUID) -> Optional[Order]:
        stmt = (
            select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
        )
        result = await self.session.execute(stmt)

        return result.unique().scalar_one_or_none()

    async def delete_order(self, order_id: uuid.UUID) -> bool:
        try:
            stmt = delete(Order).where(Order.id == order_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except IntegrityError:
            await self.session.rollback()
            raise

    async def update_order_status(
        self, order_id: uuid.UUID, status: str
    ) -> Optional[Order]:
        try:
            order = await self.get_order_by_id(order_id)
            if not order:
                return None

            order.status = status
            await self.session.commit()
            await self.session.refresh(order)
            return order

        except IntegrityError:
            await self.session.rollback()
            raise
