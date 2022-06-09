# src/models/JobShortlistModel.py
from marshmallow import fields, Schema
import datetime
from src.models.JobModel import JobModel

from . import db, bcrypt

class JobShortlistModel(db.Model):
  """
  JobShortlist Model
  """
  # table name
  __tablename__ = 'jobshortlists'

  id = db.Column(db.Integer, primary_key=True)
  talent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
  company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
  applied_at = db.Column(db.DateTime, nullable=False)
  

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.job_id = data.get('job_id')
    self.talent_id = data.get("talent_id")
    self.company_id = JobModel.get_job_by_id(self.job_id).company_id
    self.applied_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
        setattr(self, key, item)
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
    return JobShortlistModel.query.filter_by(job_id=value)
  
  @staticmethod
  def get_jobs_by_talentid(value):
    return JobShortlistModel.query.filter_by(talent_id=value)
  
  @staticmethod
  def get_by_companyid(value):
    return JobShortlistModel.query.filter_by(company_id=value)
  
  @staticmethod
  def get_by_jobid_page(value, page_num, page_length):
    return JobShortlistModel.query.filter_by(job_id=value).paginate(page=page_num, per_page=page_length, error_out=True)
  # def __generate_hash(self, password):
  #   return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  # def check_hash(self, password):
  #   return bcrypt.check_password_hash(self.password, password)
  
  # def __repr(self):
  #   return '<id {}>'.format(self.id)

class JobShortlistSchema(Schema):
  id = fields.Int(dump_only=True)
  talent_id = fields.Int(required=True)
  company_id = fields.Int(required=True)
  job_id = fields.Int(required=True)
  applied_at = fields.DateTime(dump_only=True)

