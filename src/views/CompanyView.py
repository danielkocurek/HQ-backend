#/src/views/CompanyView.py
from flask import request, Blueprint, json, Response
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

