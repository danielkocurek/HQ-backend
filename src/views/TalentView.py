#/src/views/TalentView.py
from flask import request, g, Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.CustomService import custom_response
from ..shared.Authentication import Auth
from ..models.TalentModel import TalentModel, TalentSchema
from ..models.ProfileModel import *

talent_api = Blueprint('talent_api', __name__)
talent_schema = TalentSchema()


@talent_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Talent Function
  """
  req_data = request.get_json()
  print(req_data)
  data = talent_schema.load(req_data)
  talent_in_db = TalentModel.get_talent_by_userid(data.get('user_id'))
  if talent_in_db:
    message = {'error': 'Talent already exist, please try another email address'}
    return custom_response(message, 400)
  # if error:
  #   return custom_response(error, 400)
  post = TalentModel(data)
  post.save()
  data = talent_schema.dump(post)
  data['status'] = 'success'
  return custom_response(data, 200)

@talent_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Talents
  """
  posts = TalentModel.get_all_talent()
  data = talent_schema.dump(posts, many=True)
  data['status'] = 'success'
  return custom_response(data, 200)

@talent_api.route('/by_user/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_talent_by_userid(user_id):
  """
  Get A Talent
  """
  talent = TalentModel.get_talent_by_userid(user_id)
  if not talent:
    return custom_response({'error': 'talent profile not found'}, 400)
  data = talent_schema.dump(talent)
  data['status'] = 'success'
  return custom_response(data, 200)

@talent_api.route('talents_all/<int:page_num>/<int:page_length>', methods=['GET'])
def get_all_talents(page_num, page_length):
  try:
    talents = TalentModel.get_all_talent_page_num(page_num, page_length)
  except ValidationError as error:
    print(error.messages)
    return custom_response(error, 200)
  if not talents:
    return custom_response({'error':'Any talents did not exist'}, 400)
  data_talents = talent_schema.dump(talents.items, many=True)
  res_data = []
  for talent in data_talents:
    user_id = talent.get('user_id')
    dump_data =  ProfileSchema().dump(ProfileModel.get_profile_by_userid(user_id))
    talent['talent_logo'] = dump_data.get('avator')
    talent['video_id'] = dump_data.get('video_id')
    talent['resume'] = dump_data.get('resume')
    res_data.append(talent)
  return custom_response(res_data,200)
  
  
@talent_api.route('/update/<int:id>', methods=['PUT'])
@Auth.auth_required
def update(id):
  """
  Update A Talent
  """
  req_data = request.get_json()
  talent = TalentModel.get_talent_by_id(id)
  if not talent:
    return custom_response({'error': 'talent profile not found'}, 400)
  data = talent_schema.load(req_data, partial=True)
  talent.update(data)
  
  res_data = talent_schema.dump(talent)
  res_data['status'] = 'success'
  return custom_response(res_data, 200)

@talent_api.route('/<int:id>', methods=['DELETE'])
@Auth.auth_required
def delete(id):
  """
  Delete A Talent
  """
  talent = TalentModel.get_talent_by_id(id)
  if not talent:
    return custom_response({'error': 'talent not found'}, 400)
  data = talent_schema.dump(talent)

  talent.delete()
  return custom_response({'message': 'deleted', 'status':'success'}, 200)


@talent_api.route('/talent_by_uid/<string:id>', methods=['GET'])
@Auth.auth_required
def get_talents_by_uid(id):
  talent = TalentModel.get_talent_by_uid(id)
  if not talent:
    return custom_response({'error': 'talent not found'}, 400)
  
  res_data = talent_schema.dump(talent)
  res_data['status'] = 'success'
  return custom_response(res_data, 200)    
  


