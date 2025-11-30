from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/category/v1", tags=["categories"])

@router.post("/categories", response_model=schemas.CategoryRead, status_code=201)
async def create_category(payload: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    c = await crud.create_category(db, payload)
    return await crud.get_category(db, c.id)

@router.get("/categories", response_model=List[schemas.CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_db)):
    rows = await crud.list_categories(db)
    return rows

@router.get("/categories/{category_id}", response_model=schemas.CategoryRead)
async def get_category(category_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    c = await crud.get_category(db, category_id)
    if not c:
        raise HTTPException(404, "not found")
    return c

@router.put("/categories/{category_id}", response_model=schemas.CategoryRead)
async def update_category(category_id: uuid.UUID, payload: schemas.CategoryUpdate, db: AsyncSession = Depends(get_db)):
    c = await crud.update_category(db, category_id, payload)
    if not c:
        raise HTTPException(404, "not found")
    return c

@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await crud.delete_category(db, category_id)
    return None
