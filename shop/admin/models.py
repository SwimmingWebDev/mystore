from sqlalchemy import DateTime, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from shop import db,app


class User(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False)
    email =  mapped_column(String(200), unique=False, nullable=True)
    password = mapped_column(String(200), unique=False, nullable=False)
    profile = mapped_column(String(180), unique=False, nullable=False, default='profile.jpg')


with app.app_context():
    db.create_all()
