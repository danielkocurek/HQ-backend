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
  job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
  talent_id = db.Column(db.Integer, db.ForeignKey('talents.id'), nullable=False)
  applied_at = db.Column(db.DateTime, nullable=False)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.job_id = data.get('job_id')
    self.talent_id = data.get('talent_id')
    self.applied_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # @staticmethod
  # def get_all_users():
  #   return ProfileModel.query.all()

  # @staticmethod
  # def get_one_user(id):
  #   return ProfileModel.query.get(id)
  @staticmethod
  def get_talents_by_jobid(value):
    return AppliedJobModel.query.filter_by(job_id=value)
  
  @staticmethod
  def get_jobs_by_talentid(value):
    return AppliedJobModel.query.filter_by(talent_id=value)
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
  talent_id = fields.Int(required=True)
  applied_at = fields.DateTime(dump_only=True)

