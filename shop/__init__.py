from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.instance_path = Path("data").resolve()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] = 'greenbasket'

db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt(app)

db.init_app(app)

from shop.admin import routes