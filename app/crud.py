from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, outerjoin
from sqlalchemy.orm import selectinload, aliased
from typing import List
import uuid

from . import models, schemas


async def create_cms(db: AsyncSession, data: schemas.CmsCreate) -> models.Cms:
    translation = models.Cms(code=data.code, value=data.value, language=data.language)
    db.add(translation)
    await db.commit()
    await db.refresh(translation)
    return translation


async def list_cms(db: AsyncSession) -> List[models.Cms]:
    translations = await db.execute(select(models.Cms))
    return translations.scalars().all()


async def create_category(db: AsyncSession, data: schemas.CategoryCreate) -> models.Category:
    category = models.Category(name=data.name)
    if data.children_ids:
        children = await db.execute(select(models.Category).where(models.Category.id.in_(data.children_ids)))
        category.children = children.scalars().all()
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category(db: AsyncSession, category_id: uuid.UUID) -> models.Category:
    category = await db.execute(select(models.Category).where(models.Category.id == category_id).options(
        selectinload(models.Category.children)))
    return category.scalars().first()


async def list_categories(db: AsyncSession) -> List[models.Category]:
    category = await db.execute(select(models.Category).options(selectinload(models.Category.children)))
    return category.scalars().all()


async def update_category(db: AsyncSession, category_id: uuid.UUID, data: schemas.CategoryUpdate) -> models.Category:
    category = await get_category(db, category_id)
    if category is None:
        return None
    if data.name is not None:
        category.name = data.name
    if data.children_ids is not None:
        q = await db.execute(select(models.Category).where(models.Category.id.in_(data.children_ids)))
        category.children = q.scalars().all()
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: uuid.UUID) -> None:
    await db.execute(delete(models.Category).where(models.Category.id == category_id))
    await db.commit()
    return None


async def create_product(db: AsyncSession, data: schemas.ProductCreate) -> models.Product:
    product = models.Product(
        name=data.name,
        description=data.description,
        brand=data.brand,
        code=data.code,
        stock=data.stock or 0,
        image_url=data.image_url,
        category_id=data.category_id,
        price=data.price or 0,
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_product(db: AsyncSession, product_id: uuid.UUID) -> models.Product:
    product = await db.execute(
        select(models.Product).where(models.Product.id == product_id).options(selectinload(models.Product.category)))
    first = product.scalars().first()
    description = await db.execute(select(models.Cms).where(models.Cms.code == first.description).where(models.Cms.language == "nl_BE"))
    name = await db.execute(select(models.Cms).where(models.Cms.code == first.name).where(models.Cms.language == "nl_BE"))
    first.name = name.scalars().first()
    first.description = description.scalars().first()
    return first


async def list_products(db: AsyncSession) -> List[models.Product]:
    name_cms = aliased(models.Cms)
    language = "nl_BE"
    description_cms = aliased(models.Cms)

    stmt = (
        select(models.Product, name_cms.value,
               description_cms.value)
        .outerjoin(name_cms, and_(name_cms.code == models.Product.name, name_cms.language == language))
        .outerjoin(description_cms,
                   and_(description_cms.code == models.Product.description, description_cms.language == language))
        .options(selectinload(models.Product.category))
    )

    result = await db.execute(stmt)

    products_with_translations = []
    for p, translated_name, translated_description in result.all():
        if translated_name:
            p.name = translated_name
        if translated_description:
            p.description = translated_description
        products_with_translations.append(p)

    return products_with_translations


async def update_product(db: AsyncSession, product_id: uuid.UUID, data: schemas.ProductUpdate) -> models.Product:
    product = await get_product(db, product_id)
    if product is None:
        return None
    for k, v in data.dict(exclude_unset=True).items():
        setattr(product, k, v)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product_id: uuid.UUID) -> None:
    await db.execute(delete(models.Product).where(models.Product.id == product_id))
    await db.commit()


async def create_shopping_basket(db: AsyncSession, data: schemas.ShoppingBasketCreate) -> models.ShoppingBasket:
    shopping_basket = models.ShoppingBasket()
    if data.items:
        for it in data.items:
            shopping_basket.items.append(
                models.ShoppingBasketItem(product_id=it.product_id, price=it.price or 0, amount=it.amount or 1))
    db.add(shopping_basket)
    await db.commit()
    await db.refresh(shopping_basket)
    return shopping_basket


async def get_shopping_basket(db: AsyncSession, basket_id: uuid.UUID) -> models.ShoppingBasket:
    language = "nl_BE"
    name_cms = aliased(models.Cms)

    stmt = (
        select(models.ShoppingBasket)
        .outerjoin(models.ShoppingBasket.items)
        .outerjoin(models.ShoppingBasketItem.product)
        .outerjoin(name_cms, and_(name_cms.code == models.Product.name, name_cms.language == language))
        .where(models.ShoppingBasket.id == basket_id)
        .options(
            selectinload(models.ShoppingBasket.items)
            .selectinload(models.ShoppingBasketItem.product)
            .selectinload(models.Product.category)
        )
    )

    result = await db.execute(stmt)
    shopping_basket = result.scalars().unique().first()
    if not shopping_basket:
        return None

    for item in shopping_basket.items:
        product = item.product
        if product:
            if getattr(product, 'name', None):
                translated_name = await db.scalar(
                    select(models.Cms.value).where(
                        and_(models.Cms.code == product.name, models.Cms.language == language))
                )
                if translated_name:
                    product.name = translated_name

    return shopping_basket


async def add_item_to_shopping_basket(db: AsyncSession, basket_id: uuid.UUID,
                                      item: schemas.ShoppingBasketItemCreate) -> models.ShoppingBasket:
    shopping_basket = await get_shopping_basket(db, basket_id)
    if shopping_basket is None:
        return None
    found = False
    for shopping_basket_item in shopping_basket.items:
        if shopping_basket_item.product_id == item.product_id:
            shopping_basket_item.amount += 1
            found = True
            break

    if not found:
        product = await get_product(db, item.product_id)
        new = models.ShoppingBasketItem(product_id=item.product_id, price=product.price, amount=1)
        shopping_basket.items.append(new)
        db.add(shopping_basket)
        await db.commit()
        await db.refresh(new)

    if found:
        db.add(shopping_basket)
        await db.commit()
    return shopping_basket


async def remove_item_from_shopping_basket(db: AsyncSession, item_id: uuid.UUID) -> None:
    await db.execute(delete(models.ShoppingBasketItem).where(models.ShoppingBasketItem.id == item_id))
    await db.commit()
