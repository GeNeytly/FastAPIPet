from fastapi import APIRouter, status

from api_v1.products import crud
from api_v1.products.dependencies import SessionDep, ProductDep
from api_v1.products.schemas import (
    SProduct,
    SProductCreate,
    SProductUpdate,
    SProductPartialUpdate,
)

router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[SProduct])
async def get_products(session: SessionDep):
    return await crud.get_products(session=session)


@router.post("/", response_model=SProduct)
async def create_product(product: SProductCreate, session: SessionDep):
    return await crud.create_product(session=session, product=product)


@router.get("/{product_id}/", response_model=SProduct)
async def get_product(product: ProductDep):
    return product


@router.put("/{products_id}/", response_model=SProduct)
async def update_product(
    product_update: SProductUpdate,
    session: SessionDep,
    product: ProductDep,
):
    return await crud.update_product(
        sessions=session, product=product, product_update=product_update
    )


@router.patch("/{products_id}/", response_model=SProduct)
async def partial_update_product(
    product_update: SProductPartialUpdate,
    session: SessionDep,
    product: ProductDep,
):
    return await crud.update_product(
        sessions=session, product=product, product_update=product_update, partial=True
    )


@router.delete("/{products_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(session: SessionDep, product: ProductDep):
    await crud.delete_product(sessions=session, product=product)
