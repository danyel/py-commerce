import uuid
from typing import List

from pydantic import BaseModel


class Category(BaseModel):
    id: uuid.UUID
    name: str
    children: List["Category"] = []


class Product(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    code: str
    price: float
    stock: int
    imageUrl: str
    brand: str
    category: Category

class Health (BaseModel):
    name: str
    status: str

class ProductId(BaseModel):
    id: uuid.UUID

class CreateProduct(BaseModel):
    name: str
    description: str
    code: str
    price: float
    imageUrl: str
    brand: str
    categoryId: uuid.UUID


class ShoppingBasket(BaseModel):
    id: uuid.UUID
    items: List["ShoppingBasketItem"] = []


class AddShoppingBasketItem(BaseModel):
    productId: uuid.UUID


class ShoppingBasketId(BaseModel):
    id: uuid.UUID


class ShoppingBasketItem(BaseModel):
    id: uuid.UUID
    shoppingBasket: ShoppingBasket
    productId: uuid.UUID
    amount: int
    price: float
