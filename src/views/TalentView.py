#/src/views/BlogpostView.py
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.TalentModel import TalentModel, TalentSchema

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

@talent_api.route('/<int:id>', methods=['GET'])
@Auth.auth_required
def get_one(id):
  """
  Get A Talent
  """
  talent = TalentModel.get_talent_by_id(id)
  if not talent:
    return custom_response({'error': 'talent profile not found'}, 400)
  data = talent_schema.dump(talent)
  data['status'] = 'success'
  return custom_response(data, 200)

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
  

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

