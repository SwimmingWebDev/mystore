from sqlalchemy import DateTime, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from shop import db, app

class Category(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False, unique=True)
    cat = relationship("Item", back_populates="category", cascade="all, delete-orphan")

class Item(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False, unique=True)
    price = mapped_column(Integer, nullable=True)
    quantity = mapped_column(Integer, nullable=True)
    description = mapped_column(String(500), nullable=True)
    created = mapped_column(DateTime, nullable=False, default=datetime.now().replace(microsecond=0))

    category_id = mapped_column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', back_populates="cat")
 

    photo = mapped_column(String(10), nullable=False, default='item.jpg')


with app.app_context():
    # db.drop_all()
    db.create_all()
