#src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

from .TalentModel import TalentModel, TalentSchema
from .UserModel import UserModel, UserSchema