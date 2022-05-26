# src/models/AppliedJobModel.py
from marshmallow import fields, Schema
import datetime

from . import db, bcrypt

class AppliedJobModel(db.Model):
  """
  AppliedJob Model
  """
  # table name
  __tablename__ = 'appliedjobs'

  id = db.Column(db.Integer, primary_key=True)
  job_id = db.Column(db.Integer, nullable=False)
  applied_at = db.Column(db.Datatime, nullable=False)
  on_shortlist = db.Column(db.Boolean, nullable=False)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.job_id = data.get('job_id')
    self.applied_at = data.get("applied_at")
    self.on_shortlist = data.get("on_shortlist")

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

class AppliedJobSchema(Schema):
  id = fields.Int(dump_only=True)
  job_id = fields.Int(required=True)
  applied_at = fields.DateTime(required=True)
  on_shortlist = fields.Boolean(required=True)

