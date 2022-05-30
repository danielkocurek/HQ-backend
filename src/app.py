#src/app.py

from flask import Flask, redirect, render_template, url_for, request, json, Response, flash
import os
from werkzeug.utils import secure_filename


from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.TalentView import talent_api as talent_blueprint
from .views.CompanyView import company_api as company_blueprint
from .views.JobView import job_api as job_blueprint

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}



def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  app.secret_key = "secret key"

  app.config.from_object(app_config[env_name])
  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)
  

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(talent_blueprint, url_prefix='/api/v1/talents')
  app.register_blueprint(company_blueprint, url_prefix='/api/v1/companies')
  app.register_blueprint(job_blueprint, url_prefix='/api/v1/jobs')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your part 2 endpoint is working'

  return app

