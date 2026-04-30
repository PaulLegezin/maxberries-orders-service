import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger_config import logger
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse


class OrderService:
    def __init__(self, db: AsyncSession):
        self.order_repo = OrderRepository(db)

    async def create_order(
        self, user_id: uuid.UUID, order_data: OrderCreate
    ) -> OrderResponse:
        try:
            logger.info("Запрос на создание заказа")
            order = await self.order_repo.create_order(user_id, order_data)
            logger.info("Заказ успешно создан. ID: %s", order.id)
            return order

        except Exception as e:
            logger.error("Ошибка при создании заказа: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера",
            ) from e

    async def get_order(self, order_id: uuid.UUID, user_id: uuid.UUID) -> OrderResponse:
        try:
            logger.info("Запрос на получение заказа. ID: %s", order_id)
            order = await self.order_repo.get_order_by_id(order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Заказ не найден")

            if order.user_id != user_id:
                raise HTTPException(status_code=403, detail="Доступ запрещен")

            logger.info("Заказ успешно найден")

            return order

        except HTTPException:
            raise

        except Exception as e:
            logger.error("Ошибка при получении заказа: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера",
            ) from e

    async def update_status(
        self, order_id: uuid.UUID, new_status: str, user_id: uuid.UUID
    ) -> OrderResponse:
        try:
            logger.info("Запрос на обновление статуса заказа. ID: %s", order_id)

            order = await self.get_order(order_id, user_id)
            if not order:
                raise HTTPException(status_code=404, detail="Заказ не найден")

            if order.user_id != user_id:
                raise HTTPException(status_code=403, detail="Доступ запрещен")

            updated_order = await self.order_repo.update_order_status(
                order_id, new_status
            )

            logger.info("Заказ успешно обновлен")

            return updated_order

        except HTTPException:
            raise

        except Exception as e:
            logger.error("Ошибка при обновлении заказа: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера",
            ) from e

    async def delete_order(self, order_id: uuid.UUID, user_id: uuid.UUID):
        try:
            logger.info("Запрос на удаление заказа. ID: %s", order_id)

            await self.get_order(order_id, user_id)
            is_deleted = await self.order_repo.delete_order(order_id)

            if is_deleted is False:
                raise HTTPException(status_code=400, detail="Заказ не найден")

            logger.info("Заказ успешно удален")

        except HTTPException:
            raise

        except Exception as e:
            logger.exception("Ошибка базы данных при удалении заказа: %s", str(e))
            raise HTTPException(
                status_code=500, detail="Внутренняя ошибка сервера"
            ) from e
