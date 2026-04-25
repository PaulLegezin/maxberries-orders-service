from jose import JWTError, jwt
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.token import TokenData


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return TokenData(
            user_id=user_id,
            permissions=payload.get("permissions", []),
            role=payload.get("role"),
        )
    except (JWTError, ValidationError):
        return None
