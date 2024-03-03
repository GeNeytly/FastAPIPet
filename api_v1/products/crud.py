from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import (
    SProductCreate,
    SProductUpdate,
    SProductPartialUpdate,
)
from core.models import Product
from crud import BaseCrud


class ProductCrud(BaseCrud):
    model = Product


async def create_product(session: AsyncSession, product: SProductCreate) -> Product:
    product = Product(**product.model_dump())
    session.add(product)
    await session.commit()
    return product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def update_product(
    sessions: AsyncSession,
    product: Product,
    product_update: SProductUpdate | SProductPartialUpdate,
    partial: bool = False,
) -> Product:
    for field, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, field, value)
    await sessions.commit()
    return product


async def delete_product(sessions: AsyncSession, product: Product) -> None:
    await sessions.delete(product)
    await sessions.commit()
