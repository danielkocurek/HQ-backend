#/src/views/ProfileView.py

from flask import request, json, Response, Blueprint, g
from marshmallow import ValidationError
from ..models.ProfileModel import *
from ..shared.Authentication import Auth

profile_api = Blueprint('profile_api', __name__)
profile_schema = ProfileSchema()

@profile_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  try:
    data = profile_schema.load(req_data)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
    
  profile = ProfileModel(data)
  profile.save()
  ser_data = profile_schema.dump(profile)
  print("=======================")
  print(ser_data.get('id'))
  # token = Auth.generate_token(ser_data.get('id'))
  # print(token)
  return custom_response({'status': 'success'}, 200)

 

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )