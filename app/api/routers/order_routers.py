import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user_id, get_db, oauth2_scheme
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders", tags=["Orders"], dependencies=[Depends(oauth2_scheme)]
)


@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
) -> OrderResponse:

    service = OrderService(db)
    return await service.create_order(user_id=user_id, order_data=order_data)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
) -> OrderResponse:

    service = OrderService(db)
    return await service.get_order(order_id=order_id, user_id=user_id)


@router.delete("/{order_id}", status_code=204)
async def delete_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):

    service = OrderService(db)
    await service.delete_order(order_id=order_id, user_id=user_id)
    return None


@router.patch("/{order_id}", response_model=OrderResponse)
async def update_status(
    order_id: uuid.UUID,
    new_status: str,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> OrderResponse:

    service = OrderService(db)
    return await service.update_status(
        order_id=order_id, user_id=user_id, new_status=new_status
    )
