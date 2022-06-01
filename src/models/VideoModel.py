# src/models/VideoModel.py
from msilib import sequence
from turtle import title
from marshmallow import fields, Schema
import datetime

from sqlalchemy.dialects.postgresql import ARRAY,JSON
from . import db, bcrypt

class VideoModel(db.Model):
  """
  Video Model
  """
  # table name
  __tablename__ = 'videos'

  id = db.Column(db.Integer, primary_key=True)
  v_data = db.Column(ARRAY(JSON), nullable=False)
  type = db.Column(db.String(128), nullable=False)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.v_data = data.get('v_data')
    self.type = data.get('type')

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      if key == 'password':
        self.password = self.__generate_hash(item)
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # @staticmethod
  # def get_all_users():
  #   return ProfileModel.query.all()

  @staticmethod
  def get_video(id):
    return VideoModel.query.get(id)
  
  # @staticmethod
  # def get_user_by_email(value):
  #   return ProfileModel.query.filter_by(email=value).first()

  # def __generate_hash(self, password):
  #   return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  # def check_hash(self, password):
  #   return bcrypt.check_password_hash(self.password, password)
  
  # def __repr(self):
  #   return '<id {}>'.format(self.id)

class VideoSchema(Schema):
  id = fields.Int(dump_only=True)
  v_data = fields.List(fields.Dict(keys=fields.Str()), required=True)
  type = fields.Str(required=True)

