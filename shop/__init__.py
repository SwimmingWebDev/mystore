from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path

#image upload 
from flask_uploads import IMAGES, UploadSet, configure_uploads

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.instance_path = Path("data").resolve()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] = 'greenbasket'

# image upload 
#reference: https://pypi.org/project/Flask-Reuploaded/
app.config['UPLOADED_PHOTOS_DEST'] = "shop/static/img"
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt(app)

db.init_app(app)

from shop.admin import routes
from shop.products import routes