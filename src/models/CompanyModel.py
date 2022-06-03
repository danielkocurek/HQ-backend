# src/models/CompanyModel.py
from marshmallow import fields, Schema
import datetime
from sqlalchemy.dialects.postgresql import JSON

from . import db, bcrypt

class CompanyModel(db.Model):
  """
  Company Model
  """
  # table name
  __tablename__ = 'companies'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  description = db.Column(db.String(128))
  region = db.Column(JSON)
  phone_number = db.Column(JSON)
  account_manager_name = db.Column(db.String(128), nullable=False)
  

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.user_id = data.get("user_id")
    self.description = data.get("description")
    self.region = data.get("region")
    self.phone_number = data.get("phone_number")
    self.account_manager_name = data.get("account_manager_name")

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_companies():
    return CompanyModel.query.all()

  @staticmethod
  def get_company_by_id(id):
    return CompanyModel.query.get(id)
  
  @staticmethod
  def get_company_by_userid(value):
    return CompanyModel.query.filter_by(user_id=value).first()

  # def __generate_hash(self, password):
  #   return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  # def check_hash(self, password):
  #   return bcrypt.check_password_hash(self.password, password)
  
  # def __repr(self):
  #   return '<id {}>'.format(self.id)

class CompanySchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  user_id = fields.Int(required=True)
  description = fields.Str()
  phone_number = fields.Dict(keys=fields.Str(), values=fields.Str())
  region = fields.Dict(keys=fields.Str(), values=fields.Str(), required = True)
  account_manager_name = fields.Str(required=True)

