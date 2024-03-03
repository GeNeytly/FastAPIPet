from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from core.models import Base

if TYPE_CHECKING:
    from core.models import Product
    from core.models import OrderProductAssociation


class Order(Base):
    _repr_cols_num = 3

    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )

    # products: Mapped[list["Product"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="orders",
    # )
    products_associations: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
