# app/main.py
from fastapi import FastAPI
from .database import engine
from .models import Base
from .router import cms, category, product, shopping_basket

app = FastAPI(title="My Shop API")

app.include_router(cms.router, prefix="/api")
app.include_router(category.router, prefix="/api")
app.include_router(product.router, prefix="/api")
app.include_router(shopping_basket.router, prefix="/api")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # create tables if not exists (dev convenience)
        await conn.run_sync(Base.metadata.create_all)
