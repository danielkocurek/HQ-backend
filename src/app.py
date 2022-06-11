#src/app.py

from flask import Flask
import os
from sqlalchemy import true
from werkzeug.utils import secure_filename


from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.TalentView import talent_api as talent_blueprint
from .views.CompanyView import company_api as company_blueprint
from .views.JobView import job_api as job_blueprint
from .views.VideoView import video_api as video_blueprint
from .views.ProfileView import profile_api as profile_blueprint
from .views.AppliedJobView import appliedjob_api as appliedjob_blueprint
from flask_cors import CORS

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}



def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)
  CORS(app, supports_credentials=true, )
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
  app.register_blueprint(video_blueprint, url_prefix='/api/v1/videos')
  app.register_blueprint(profile_blueprint, url_prefix='/api/v1/profiles')
  app.register_blueprint(appliedjob_blueprint, url_prefix='/api/v1/appliedjobs')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your part 2 endpoint is working'
  
  
  # @app.after_request
  # def after_request(response):
  #   response.headers.add('Access-Control-Allow-Origin', "*")
  #   response.headers.add('Access-Control-Allow-Credentials', True)
  #   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,api-token,X-Requested-With, Accept, X-HTTP-Method-Override')
  #   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  #   return response


  # @app.before_request
  # def before_request(response):
  #   response.headers.add('Access-Control-Allow-Origin', '')
  #   response.headers.add('Access-Control-Allow-Credentials', True)
  #   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,api-key,X-Requested-With')
  #   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  #   return response
  return app

