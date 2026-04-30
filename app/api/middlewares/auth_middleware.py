from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logger_config import logger
from app.core.security import decode_token

PERMISSION_MAP = {
    ("/orders", "POST"): "orders.create",
    ("/orders", "DELETE"): "orders.delete",
    ("/orders", "PATCH"): "orders.update_status",
}


async def unified_auth_middleware(request: Request, call_next):
    request.state.user_id = None
    request.state.user_role = None
    request.state.permissions = []

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        try:
            token_data = decode_token(token)
            if token_data:
                request.state.user_id = token_data.user_id
                request.state.permissions = token_data.permissions

                request.state.user_role = getattr(token_data, "role", None)
        except Exception as e:
            logger.warning("Ошибка декодирования токена: %s", str(e))

    logger.info(
        "User %s | Role %s | Path %s",
        request.state.user_id or "Anonymous",
        request.state.user_role or "None",
        request.url.path,
    )

    if str(request.state.user_role).lower() in ["admin", "administrator"]:
        return await call_next(request)

    current_path = request.url.path.rstrip("/")
    if current_path == "":
        current_path = "/"
    method = request.method

    required_permission = PERMISSION_MAP.get((current_path, method))
    if required_permission:
        if required_permission not in request.state.permissions:
            return JSONResponse(
                status_code=403,
                content={
                    "detail": f"Недостаточно прав. Требуется: {required_permission}"
                },
            )

    return await call_next(request)
