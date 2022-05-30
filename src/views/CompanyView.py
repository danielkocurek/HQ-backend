#/src/views/CompanyView.py
from flask import redirect, render_template, request, g, Blueprint, json, Response, url_for
from ..shared.Authentication import Auth
from ..models.CompanyModel import *
from werkzeug.utils import secure_filename
import os

company_api = Blueprint('company_api', __name__)
company_schema = CompanySchema()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@company_api.route('/video', methods=['POST'])
@Auth.auth_required
def upload_file():
  print(request.method) 
  if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
          return custom_response({'error': "this is not file "}, 400)
      file = request.files['file']
      print(file.filename)
      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
          return custom_response({'error': "this is not allowed file "}, 400)
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          print(os.path.join('src/static/uploads', filename))
          file.save(os.path.join('src/static/uploads', filename))
          return custom_response({'status': "success "}, 200)
  return custom_response({'status1': "success "}, 200)
          
@company_api.route('/display/<filename>')
# @Auth.auth_required
def display_video(filename):
  #print('display_video filename: ' + filename)
  return redirect(url_for('static', filename='uploads/' + filename), code=301)


@company_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Company profile
  """
  req_data = request.get_json()
  data = company_schema.load(req_data)
  # if error:
  #   return custom_response(error, 400)
  company = CompanyModel(data)
  company.save()
  data = company_schema.dump(company)
  return custom_response(data, 201)

@company_api.route('/update/<int:id>', methods=['PUT'])
@Auth.auth_required
def update(id):
  """
    Update Company Profile
  Returns:
      Updated Company Profile
  """
  req_data = request.get_json()
  data = company_schema.load(req_data)
  company = CompanyModel.get_company_by_id(id)
  company.update(data)
  res_company = company_schema.dump(company)
  return custom_response(res_company, 200)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

