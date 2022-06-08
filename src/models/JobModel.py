# src/models/JobModel.py
from marshmallow import fields, Schema
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import ARRAY
import datetime
from .ProfileModel import ProfileModel
from .CompanyModel import CompanyModel 

from . import db, bcrypt

class JobModel(db.Model):
  """
  Job Model
  """
  # table name
  __tablename__ = 'jobs'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  region = db.Column(JSON, nullable=False)
  experience_year = db.Column(db.String(128), nullable=False)
  education = db.Column(db.String(128), nullable=False)
  salary = db.Column(db.String(128))
  department = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  description = db.Column(db.Text)
  job_status = db.Column(db.String(128))
  company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
  roles = db.Column(ARRAY(db.String(128)), nullable=False)

  

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.title = data.get("title")
    self.region = data.get("region")
    self.experience_year = data.get("experience_year")
    self.education = data.get("education")
    self.salary = data.get("salary")
    self.department = data.get("department")
    self.description = data.get("description")
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
    self.job_status = "hiring"
    self.company_id = data.get('company_id')
    self.roles = data.get("roles")
    
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
  def get_job_by_id(id):
    return JobModel.query.get(id)
  
  @staticmethod
  def get_all_job_by_companyid(id):
    return JobModel.query.filter_by(company_id=id)
  
  @staticmethod
  def get_all_jobs():
    return JobModel.query.all()
  
  @staticmethod
  def get_all_jobs_by_pagination(page_num, page_length):
    return JobModel.query.paginate(per_page=page_length, page=page_num, error_out=True)  
  
  @staticmethod
  def get_companylogo(id):
    user_id = CompanyModel.query.get(id).user_id
    if ProfileModel.query.filter_by(user_id=user_id).first():
      return ProfileModel.query.filter_by(user_id=user_id).first().avator
    else:
      return ''

  @staticmethod
  def get_companyvideo(id):
    user_id = CompanyModel.query.get(id).user_id
    if ProfileModel.query.filter_by(user_id=user_id).first(): 
      return ProfileModel.query.filter_by(user_id=user_id).first().video
    else:
      return ''
  
  @staticmethod
  def get_companyname(id):
    return CompanyModel.query.get(id).name
  
class JobSchema(Schema):
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  region = fields.Dict(required=True)
  experience_year = fields.Str(required=True)
  education = fields.Str(required=True)
  salary = fields.Str()
  department = fields.Str(required=True)
  description = fields.Str()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  job_status =  fields.Str() 
  company_id = fields.Int(required=True)
  roles = fields.List(fields.String(), required=True)

