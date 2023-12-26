from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class SCreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(25)]
    email: EmailStr
