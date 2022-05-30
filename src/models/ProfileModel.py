# src/models/ProfileModel.py
from marshmallow import fields, Schema
import datetime

from . import db, bcrypt

class ProfileModel(db.Model):
  """
  Profile Model
  """
  # table name
  __tablename__ = 'profiles'

  id = db.Column(db.Integer, primary_key=True)
  avator = db.Column(db.String(128), nullable=False)
  resume = db.Column(db.String(128), nullable=False)
  video = db.Column(db.String(128), nullable=False)
  target_id = db.Column(db.Integer)
  type = db.Column(db.String(128))

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.avator = data.get('avator')
    self.resume = data.get("resume")
    self.video = data.get("video")
    self.target_id = data.get("target_id")
    self.type = data.get('type')

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

class ProfileSchema(Schema):
  id = fields.Int(dump_only=True)
  avator = fields.Str(required=True)
  resume = fields.Str(required=True)
  video = fields.Str(required=True)
  target_id = fields.Int(required=True)
  type = fields.Str(required=True)

