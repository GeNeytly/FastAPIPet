from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import UserRelationMixin


if TYPE_CHECKING:
    from .user import User


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id!r})"

    def __repr__(self):
        return str(self)
