import uuid
from decimal import Decimal

import httpx
from fastapi import HTTPException

CATALOG_SERVICE_URL = "http://fastapi_catalog_service:8000"


async def get_product_price(product_id: uuid.UUID) -> Decimal:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CATALOG_SERVICE_URL}/products/{product_id}")
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404, detail=f"Товар {product_id} не найден в каталоге"
                )

            product_data = response.json()
            return Decimal(product_data["price"])

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503, detail=f"Catalog Service недоступен: {exc}"
            ) from exc
