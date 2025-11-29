from typing import List
from fastapi import HTTPException, APIRouter
from app.schemas import Product, ShoppingBasket, AddShoppingBasketItem, ProductId, Health

router = APIRouter()


@router.get(
    '/api/product/v1/products',
    response_model=List[Product],
    tags=['product'],
    description='Get all products',
    operation_id='get_products',
    status_code=200,
)
async def get_products():
    return None


@router.post(
    '/api/product/v1/products',
    response_model=ProductId,
    tags=['product'],
    description='Create a new product',
    status_code=201,
    operation_id='create_product',
)
async def create_product(product: Product):
    return None


@router.get(
    '/api/product/v1/products/{product_id}',
    response_model=Product,
    tags=['product'],
    description='Get a product',
    operation_id='get_product',
    status_code=200
)
async def get_product_by_id(product_id: int):
    return None


@router.post(
    '/api/shopping-basket/v1/shopping-baskets',
    response_model=ShoppingBasket,
    tags=['shopping-basket'],
    description='Shopping basket',
    operation_id='create_shopping_basket',
    status_code=201
)
async def create_shopping_basket():
    return None


@router.get(
    '/api/shopping-basket/v1/shopping-baskets/{shopping_basket_id}',
    response_model=ShoppingBasket,
    tags=['shopping-basket'],
    description='Get shopping basket',
    operation_id='get_shopping_basket',
    status_code=200
)
async def get_shopping_basket(shopping_basket_id: int):
    return None


@router.post(
    '/api/shopping-basket/v1/shopping-baskets/{shopping_basket_id}',
    response_model=ShoppingBasket,
    tags=['shopping-basket'],
    description='Adds a product to the shopping basket',
    operation_id='add_shopping_basket_item',
    status_code=200
)
async def add_shopping_basket_item(shopping_basket_id: int, add_shopping_basket_item: AddShoppingBasketItem):
    return None


@router.get(
    '/api/health',
    tags=['health'],
    description='Health check',
    status_code=200,
    response_model=List[Health]
)
async def ping_pong():
    items = []
    item = Health(name="name",status = "ok")
    items.append(item)
    return items
