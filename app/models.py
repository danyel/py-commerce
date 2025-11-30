import uuid

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Cms(Base):
    __tablename__ = 'cms'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    code = Column(String)
    value = Column(String)
    language = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


category_children = Table(
    'category_children',
    Base.metadata,
    Column('parent_id', UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True),
    Column('child_id', UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True)
)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String)

    # noinspection PyTypeChecker
    children = relationship(
        "Category",
        secondary=category_children,
        primaryjoin=id == category_children.c.parent_id,
        secondaryjoin=id == category_children.c.child_id,
        backref="parents",
        cascade="all, delete"
    )

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)



class Product(Base):
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String)
    description = Column(String)
    brand = Column(String)
    code = Column(String)
    stock = Column(Integer, default=0)
    image_url = Column(String)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    price = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    category = relationship("Category")


class ShoppingBasket(Base):
    __tablename__ = 'shopping_basket'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)

    items = relationship(
        "ShoppingBasketItem",
        back_populates="basket",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def total_price_exclusive(self):
        return self.total_price_inclusive / 1.21

    @property
    def tax(self):
        return self.total_price_inclusive - self.total_price_exclusive

    @property
    def total_price_inclusive(self):
        return sum(item.price * item.amount for item in self.items)

class ShoppingBasketItem(Base):
    __tablename__ = 'shopping_basket_items'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)

    shopping_basket_id = Column(
        UUID(as_uuid=True),
        ForeignKey("shopping_basket.id"),
        nullable=False
    )

    price = Column(Integer)
    amount = Column(Integer)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))

    basket = relationship(
        "ShoppingBasket",
        back_populates="items"
    )
    product = relationship("Product")

    @property
    def image_url(self):
        return self.product.image_url
    @property
    def name(self):
        return self.product.name
