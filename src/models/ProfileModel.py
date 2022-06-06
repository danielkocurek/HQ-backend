# src/models/ProfileModel.py
from marshmallow import fields, Schema
import datetime
from sqlalchemy.dialects.postgresql import ARRAY


from . import db, bcrypt

class ProfileModel(db.Model):
  """
  Profile Model
  """
  # table name
  __tablename__ = 'profiles'

  id = db.Column(db.Integer, primary_key=True)
  avator = db.Column(db.String(256))
  resume = db.Column(db.String(256))
  video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
  video = db.Column(db.String(256))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  job = db.Column(ARRAY(db.Integer))
  work_history = db.Column(ARRAY(db.String(128)))
  type = db.Column(db.String(128))

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.avator = data.get('avator')
    self.resume = data.get("resume")
    self.video_id = data.get("video_id")
    self.video = data.get('video')
    self.user_id = data.get("user_id")
    self.job = data.get("job")
    self.work_history = data.get("work_history")
    self.type = data.get('type')

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

  @staticmethod
  def get_profile_by_id(id):
    return ProfileModel.query.get(id)
  
  @staticmethod
  def get_profile_by_userid(value):
    return ProfileModel.query.filter_by(user_id=value).first()

  # def __generate_hash(self, password):
  #   return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  # def check_hash(self, password):
  #   return bcrypt.check_password_hash(self.password, password)
  
  # def __repr(self):
  #   return '<id {}>'.format(self.id)

class ProfileSchema(Schema):
  id = fields.Int(dump_only=True)
  avator = fields.Str(allow_none = True)
  resume = fields.Str(allow_none = True)
  video_id = fields.Int(allow_none = True)
  video = fields.Str(allow_none = True)
  job = fields.List(fields.Int())
  user_id = fields.Int(required=True)
  work_history = fields.List(fields.String())
  type = fields.Str(required=True)

