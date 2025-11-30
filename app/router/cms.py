from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/cms/v1", tags=["cms"])

@router.post("/translations", response_model=schemas.CmsRead, status_code=201)
async def create_cms(payload: schemas.CmsCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_cms(db, payload)

@router.get("/translations", response_model=List[schemas.CmsRead])
async def list_cms(db: AsyncSession = Depends(get_db)):
    return await crud.list_cms(db)
