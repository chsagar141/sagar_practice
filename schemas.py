from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str
    price: int
    available: bool = True


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
