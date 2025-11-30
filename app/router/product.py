from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/product/v1", tags=["products"])

@router.post("/products", response_model=schemas.ProductRead, status_code=201)
async def create_product(payload: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    p = await crud.create_product(db, payload)
    return p

@router.get("/products", response_model=List[schemas.ProductRead])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await crud.list_products(db)

@router.get("/{product_id}", response_model=schemas.ProductRead)
async def get_product(product_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    p = await crud.get_product(db, product_id)
    if not p:
        raise HTTPException(404, "not found")
    return p

@router.put("/{product_id}", response_model=schemas.ProductRead)
async def update_product(product_id: uuid.UUID, payload: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)):
    p = await crud.update_product(db, product_id, payload)
    if not p:
        raise HTTPException(404, "not found")
    return p

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await crud.delete_product(db, product_id)
    return None
