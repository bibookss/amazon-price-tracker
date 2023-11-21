from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    items = relationship("UserItem", back_populates="user")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    rating = Column(Float, index=True)
    price = Column(Float, index=True)
    url = Column(String(255), index=True)
    image = Column(String(255), index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("UserItem", back_populates="item")
    prices = relationship("ItemPrice", back_populates="item")

class UserItem(Base):
    __tablename__ = "user_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="items")
    item = relationship("Item", back_populates="users")

class ItemPrice(Base):
    __tablename__ = "item_prices"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    price = Column(Float, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    item = relationship("Item", back_populates="prices")