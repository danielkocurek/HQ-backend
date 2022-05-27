# src/models/JobModel.py
from marshmallow import fields, Schema
from sqlalchemy.dialects.postgresql import ARRAY
import datetime

from . import db, bcrypt

class JobModel(db.Model):
  """
  Job Model
  """
  # table name
  __tablename__ = 'jobs'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  description = db.Column(db.String(128), nullable=False)
  post_at = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False)
  status = db.Column(db.String(128), nullable=False)
  candidates = db.Column(ARRAY(db.String(128)), nullable=False)

  

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.title = data.get("title")
    self.description = data.get("description")
    self.post_at = data.get("post_at")
    self.updated_at = data.get("updated_at")
    self.status = data.get("status")
    self.candidates = data.get("candidates")
    
  def save(self):
    db.session.add(self)
    db.session.commit()

  # def update(self, data):
  #   for key, item in data.items():
  #     if key == 'password':
  #       self.password = self.__generate_hash(item)
  #     setattr(self, key, item)
  #   self.modified_at = datetime.datetime.utcnow()
  #   db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # @staticmethod
  # def get_all_users():
  #   return ProfileModel.query.all()

  # @staticmethod
  # def get_one_user(id):
  #   return ProfileModel.query.get(id)
  
  # @staticmethod
  # def get_user_by_email(value):
  #   return ProfileModel.query.filter_by(email=value).first()

  # def __generate_hash(self, password):
  #   return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  # def check_hash(self, password):
  #   return bcrypt.check_password_hash(self.password, password)
  
  # def __repr(self):
  #   return '<id {}>'.format(self.id)

class CompanySchema(Schema):
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  description = fields.Str(required=True)
  post_at = fields.DateTime(required=True)
  updated_at = fields.DateTime(required=True)
  status = fields.Str(required=True)
  candidates = fields.Dict(required=True)

