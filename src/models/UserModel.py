# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime
from random import randrange

from . import db, bcrypt
# import enum

# class UserTypes(enum.Enum):
#   TALENT = "Talent"
#   COMPANY = "Company"
#   ADMIN = "Admin"

#   @classmethod
#   def choices(cls):
#     return [(choice, choice.value) for choice in cls]

#   @classmethod
#   def coerce(cls, item):
#     """item will be both type(enum) AND type(unicode).
#     """
#     if item == 'Talent' or item == UserTypes.TALENT:
#         return UserTypes.TALENT
#     elif item == 'Company' or item == UserTypes.COMPANY:
#         return UserTypes.COMPANY
#     elif item == 'Admin' or item == UserTypes.ADMIN:
#         return UserTypes.ADMIN
#     else:
#         print
#         "Can't coerce", item, type(item)

#   @classmethod
#   def from_name(cls, name):
#     for estado, estado_name in UserTypes.choices():
#       if estado_name == name or name == str(estado):
#           return estado
#     raise ValueError('{} is not a valid EstadoCita name'.format(name))


class UserModel(db.Model):
  """
  User Model
  """
  # table name
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  verify_code = db.Column(db.Integer)
  register_status = db.Column(db.Boolean)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  type = db.Column(db.String(128))

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.email = data.get('email')
    self.password = self.__generate_hash(data.get('password'))
    self.verify_code = randrange(1000,9999,4)
    self.register_status = False
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
    self.type = data.get('type')

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      if key == 'password':
        item = self.__generate_hash(item)
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_users():
    return UserModel.query.all()

  @staticmethod
  def get_one_user(id):
    return UserModel.query.get(id)
  
  @staticmethod
  def get_user_by_email(value):
    return UserModel.query.filter_by(email=value).first()
  
  @staticmethod
  def get_talents_by_page_num(page_num, page_length):
    return UserModel.query.filter_by(type='talent').paginate(per_page=page_length, page=page_num, error_out=True)

  @staticmethod
  def get_companies_by_page_num(page_num, page_length):
    return UserModel.query.filter_by(type='company').paginate(per_page=page_length, page=page_num, error_out=True)
  
  @staticmethod
  def get_companies_count():
    return UserModel.query.filter_by(type='company').count()
  
  @staticmethod
  def get_talents_count():
    return UserModel.query.filter_by(type='talent').count()

  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)
  
  def __repr(self):
    return '<id {}>'.format(self.id)

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True)
  verify_code = fields.Int()
  register_status = fields.Bool()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  type = fields.Str(required=True)

