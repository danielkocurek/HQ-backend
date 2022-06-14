# src/models/TalentModel.py
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
import enum
from sqlalchemy.dialects.postgresql import JSON

# class UserTypes(enum.Enum):
#   TALENT = "Talent"
#   COMPANY = "Company"

class TalentModel(db.Model):
    """
    User Model
    """
    # table name
    __tablename__ = 'talents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(128), nullable = False)
    last_name = db.Column(db.String(128), nullable=False)
    uuid = db.Column(db.String(128))
    phone_number = db.Column(JSON)
    region = db.Column(JSON)
    current_jobTitle = db.Column(db.String(128))
    company = db.Column(db.String(128))
    current_jobDescription = db.Column(db.Text)
    years_experience = db.Column(db.String(128))
    education = db.Column(db.String(128))

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.user_id = data.get('user_id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.uuid = data.get('uuid')
        self.phone_number = data.get('phone_number')
        self.region = data.get('region')
        self.current_jobDescription = data.get('current_jobDescription')
        self.company = data.get('company')
        self.current_jobTitle = data.get('current_jobTitle')
        self.years_experience = data.get('years_experience')
        self.education = data.get('education')

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

    @staticmethod
    def get_all_talent():
        return TalentModel.query.all()
    
    @staticmethod
    def get_talents_count():
        return TalentModel.query.count()

    @staticmethod
    def get_all_talent_page_num(page_num, page_length):
        return TalentModel.query.paginate(per_page=page_length, page=page_num, error_out=True)
    
    @staticmethod
    def get_talent_by_id(id):
        return TalentModel.query.get(id)
    
    @staticmethod
    def get_talent_by_userid(value):
        return TalentModel.query.filter_by(user_id=value).first()
    
    @staticmethod
    def get_talent_by_uid(value):
     return TalentModel.query.filter_by(uuid=value).first()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def __repr(self):
        return '<id {}>'.format(self.id)

class TalentSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required = True)
    first_name = fields.Str(required = True)
    last_name = fields.Str(required = True)
    uuid = fields.Str(allow_none = True)
    phone_number = fields.Dict(keys=fields.Str(), values=fields.Str())
    current_jobTitle = fields.Str()
    company = fields.Str()
    current_jobDescription = fields.Str(required = False)
    region = fields.Dict(keys=fields.Str(), values=fields.Str())
    years_experience = fields.Str(allow_none=True)
    years_experience = fields.Str(allow_none=True)
    education = fields.Str(allow_none=True)

