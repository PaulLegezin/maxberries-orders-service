import uuid
from typing import List, Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: uuid.UUID
    permissions: List[str] = []
    role: Optional[str] = None
