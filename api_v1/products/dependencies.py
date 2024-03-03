from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from core.models import db_helper, Product


SessionDep = Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)]


async def product_by_id(
    product_id: Annotated[int, Path(ge=0)],
    session: SessionDep,
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product is None:
        error_msg = f"Product with id {product_id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)

    return product


ProductDep = Annotated[Product, Depends(product_by_id)]
