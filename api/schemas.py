from pydantic import BaseModel
from datetime import datetime
from typing import Optional 

class ItemBase(BaseModel):
    url: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    title: Optional[str] = None
    rating: Optional[float] = None
    price: Optional[float] = None
    url: str
    image: Optional[str] = None
    date_created: datetime
    prices: list['ItemPrice'] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    items: list[Item] = []
    date_created: datetime

    class Config:
        orm_mode = True

class UserItemBase(BaseModel):
    user_id: int
    item_id: int
    date_created: datetime

class UserItemCreate(UserItemBase):
    pass

class UserItem(UserItemBase):
    id: int
    user: User
    item: Item

    class Config:
        orm_mode = True

class ItemPriceBase(BaseModel):
    item_id: int
    price: float

class ItemPriceCreate(ItemPriceBase):
    pass

class ItemPrice(ItemPriceBase):
    id: int
    item: Item
    date_created: datetime

    class Config:
        orm_mode = True