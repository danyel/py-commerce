from fastapi import APIRouter, Depends, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/shopping-basket/v1", tags=["shopping basket"])

@router.post("/shopping-baskets", response_model=schemas.ShoppingBasketId, status_code=201)
async def create_basket(payload: schemas.ShoppingBasketCreate, db: AsyncSession = Depends(get_db)):
    shopping_basket = await crud.create_shopping_basket(db, payload)
    return await crud.get_shopping_basket(db, shopping_basket.id)

@router.get("/shopping-baskets/{basket_id}", response_model=schemas.ShoppingBasketRead)
async def get_basket(basket_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    shopping_basket = await crud.get_shopping_basket(db, basket_id)
    if not shopping_basket:
        raise HTTPException(404, "not found")
    return shopping_basket

@router.post("/shopping-baskets/{basket_id}", response_model=schemas.ShoppingBasketRead, status_code=200)
async def add_item(basket_id: uuid.UUID, payload: schemas.ShoppingBasketItemCreate, db: AsyncSession = Depends(get_db)):
    shopping_basket = await crud.add_item_to_shopping_basket(db, basket_id, payload)
    if not shopping_basket:
        raise HTTPException(404, "basket not found")
    return shopping_basket

@router.delete("/shopping-baskets/items/{item_id}", status_code=204)
async def remove_item(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await crud.remove_item_from_shopping_basket(db, item_id)
    return None
