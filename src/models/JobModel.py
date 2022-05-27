# src/models/JobModel.py
from marshmallow import fields, Schema
from sqlalchemy import JSON
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
  region = db.Column(JSON, nullable=False)
  experience_year = db.Column(db.String(128), nullable=False)
  education = db.Column(db.String(128), nullable=False)
  salary = db.Column(db.String(128))
  department = db.Column(db.String(128), nullable=False)
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
    self.roles = data.get("roles")
    
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

  @staticmethod
  def get_job_by_id(id):
    return JobModel.query.get(id)
class JobSchema(Schema):
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  region = fields.Dict(required=True)
  experience_year = fields.Str(required=True)
  education = fields.Str(required=True)
  salary = fields.Str()
  department = fields.Str(required=True)
  roles = fields.List(fields.String(), required=True)

