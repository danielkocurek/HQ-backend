#src/app.py

from flask import Flask

from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.TalentView import talent_api as talent_blueprint
from .views.CompanyView import company_api as company_blueprint


def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])
  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)
  

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(talent_blueprint, url_prefix='/api/v1/talents')
  app.register_blueprint(company_blueprint, url_prefix='/api/v1/companies')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your part 2 endpoint is working'

  return app

