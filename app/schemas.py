from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime


class CmsCreate(BaseModel):
    code: str
    value: str
    language: str


class CmsRead(CmsCreate):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CategoryCreate(BaseModel):
    name: str
    children_ids: Optional[List[uuid.UUID]] = Field(default_factory=list)


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    children_ids: Optional[List[uuid.UUID]] = None


class CategoryRead(BaseModel):
    id: uuid.UUID
    name: str
    children: List['CategoryRead'] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CategoryReadSimple(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    code: Optional[str] = None
    stock: Optional[int] = 0
    image_url: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    price: Optional[int] = 0


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    brand: Optional[str]
    code: Optional[str]
    stock: Optional[int]
    image_url: Optional[str]
    category_id: Optional[uuid.UUID]
    price: Optional[int]


class ProductRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    brand: Optional[str]
    code: Optional[str]
    stock: int
    image_url: Optional[str]
    category: Optional[CategoryReadSimple] = None
    price: int

    class Config:
        orm_mode = True


class ShoppingBasketItemBase(BaseModel):
    price: Optional[int] = 0
    amount: Optional[int] = 1
    image_url: Optional[str] = None
    name: Optional[str] = None


class ShoppingBasketItemCreate(BaseModel):
    product_id: Optional[uuid.UUID]


class ShoppingBasketItemRead(ShoppingBasketItemBase):
    id: uuid.UUID
    product_id: uuid.UUID
    product: Optional[ProductRead] = None

    class Config:
        orm_mode = True


class ShoppingBasketCreate(BaseModel):
    items: Optional[List[ShoppingBasketItemCreate]] = []


class ShoppingBasketId(BaseModel):
    id: uuid.UUID


class ShoppingBasketRead(BaseModel):
    id: uuid.UUID
    items: List[ShoppingBasketItemRead] = []
    total_price_exclusive: Optional[float] = 0.0
    total_price_inclusive: Optional[float] = 0.0
    tax: Optional[float] = 0.0

    class Config:
        orm_mode = True


CategoryRead.update_forward_refs()
