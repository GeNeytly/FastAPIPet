from pydantic import BaseModel, ConfigDict


class SProductBase(BaseModel):
    name: str
    description: str
    price: int


class SProductCreate(SProductBase):
    pass


class SProductUpdate(SProductBase):
    pass


class SProductPartialUpdate(SProductBase):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class SProduct(SProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
