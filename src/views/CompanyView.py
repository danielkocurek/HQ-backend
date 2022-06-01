#/src/views/CompanyView.py
from flask import request, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..models.CompanyModel import *

company_api = Blueprint('company_api', __name__)
company_schema = CompanySchema()


@company_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Company profile
  """
  req_data = request.get_json()
  try:
    data = company_schema.load(req_data)
  except ValidationError as error:
    print(error.messages)
    return custom_response(error,400)
  company_in_db = CompanyModel.get_company_by_userid(data.get('user_id'))
  if company_in_db:
    message = {'error': 'Company profile already exist, please try another email address'}
    return custom_response(message, 400)    
  # if error:
  #   return custom_response(error, 400)
  company = CompanyModel(data)
  company.save()
  data = company_schema.dump(company)
  data['status'] = 'success';
  return custom_response(data, 200)

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
  res_company['status'] = 'success'
  return custom_response(res_company, 200)

@company_api.route('/<int:id>')
@Auth.auth_required
def get_company(id):
  """
  Get a single company
  """
  company = CompanyModel.get_company_by_id(id)
  if not company:
    return custom_response({'error': 'company not found'}, 400)
  
  res_data = company_schema.dump(company)
  res_data['status'] = 'success'
  return custom_response(res_data, 200)


@company_api.route('company_by_user/<int:id>')
@Auth.auth_required
def get_company_by_user(id):
  """
  Get a single company
  """
  company = CompanyModel.get_company_by_userid(id)
  if not company:
    return custom_response({'error': 'company not found'}, 400)
  
  res_data = company_schema.dump(company)
  res_data['status'] = 'success'
  return custom_response(res_data, 200)


@company_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all_company():
  """
  Get a single company
  """
  company = CompanyModel.get_all_companies()
  if not company:
    return custom_response({'error': 'company not found'}, 400)
  
  res_data = company_schema.dump(company, many=True)
  # res_data['status'] = 'success'
  return custom_response({'res_data':res_data, 'status':'success'}, 200)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

