# src/models/AppliedJobModel.py
from marshmallow import fields, Schema
import datetime

from src.models.JobModel import JobModel

from . import db, bcrypt

class AppliedJobModel(db.Model):
  """
  AppliedJob Model
  """
  # table name
  __tablename__ = 'appliedjobs'

  id = db.Column(db.Integer, primary_key=True)
  job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
  talent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
  shortlist_status = db.Column(db.Boolean)
  applied_at = db.Column(db.DateTime, nullable=False)
  shortlist_at = db.Column(db.DateTime)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.job_id = data.get('job_id')
    self.talent_id = data.get('talent_id')
    self.applied_at = datetime.datetime.utcnow()
    self.company_id = JobModel.get_job_by_id(self.job_id).company_id
    self.shortlist_status = False
    self.shortlist_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.shortlist_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # @staticmethod
  # def get_all_users():
  #   return ProfileModel.query.all()

  @staticmethod
  def get_one(id):
    return AppliedJobModel.query.get(id)
  
  @staticmethod
  def get_by_jobid(value):
    return AppliedJobModel.query.filter_by(job_id=value).all()
  
  @staticmethod
  def get_by_talentid(value):
    return AppliedJobModel.query.filter_by(talent_id=value).all()
  
  @staticmethod
  def get_shortlist_job_by_talentid(value):
    return AppliedJobModel.query.filter_by(talent_id=value, shortlist_status=True).all()
  
  @staticmethod
  def get_by_companyid(value):
    return AppliedJobModel.query.filter_by(company_id=value).all()
  
  @staticmethod
  def get_by_companyid_page(value, page_num, page_length):
    return db.session.query(AppliedJobModel.job_id).filter_by(company_id=value).group_by(AppliedJobModel.job_id).paginate(page=page_num, per_page=page_length, error_out=True)
  
  @staticmethod
  def get_by_shortlist_companyid_page(value, page_num, page_length):
    return db.session.query(AppliedJobModel.job_id).filter_by(company_id=value, shortlist_status=True).group_by(AppliedJobModel.job_id).paginate(page=page_num, per_page=page_length, error_out=True)
  
  @staticmethod
  def get_by_jobid_page(value, page_num, page_length):
    return AppliedJobModel.query.filter_by(job_id=value).paginate(page=page_num, per_page=page_length, error_out=True)
  
  @staticmethod
  def get_by_shortlist_jobid_page(value, page_num, page_length):
    return AppliedJobModel.query.filter_by(job_id=value, shortlist_status=True).paginate(page=page_num, per_page=page_length, error_out=True)
  
  @staticmethod
  def get_jobcount_by_user(value):
    return AppliedJobModel.query.filter_by(talent_id=value).count()
  
  @staticmethod
  def get_shortlist_jobcount_by_user(value):
    return AppliedJobModel.query.filter_by(talent_id=value, shortlist_status=True).count()
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
  job_id = fields.Int(allow_none = True)
  talent_id = fields.Int(allow_none = True)
  company_id = fields.Int(allow_none = True)
  shortlist_status = fields.Bool(allow_none = True)
  applied_at = fields.DateTime(dump_only=True)
  shortlist_at = fields.DateTime(allow_none = True)

