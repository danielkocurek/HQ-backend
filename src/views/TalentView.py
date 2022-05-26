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
  req_data['owner_id'] = g.user.get('id')
  data, error = talent_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  post = TalentModel(data)
  post.save()
  data = talent_schema.dump(post).data
  return custom_response(data, 201)

@talent_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Talents
  """
  posts = TalentModel.get_all_blogposts()
  data = talent_schema.dump(posts, many=True).data
  return custom_response(data, 200)

@talent_api.route('/<int:blogpost_id>', methods=['GET'])
def get_one(blogpost_id):
  """
  Get A Talent
  """
  post = TalentModel.get_one_blogpost(blogpost_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = talent_schema.dump(post).data
  return custom_response(data, 200)

@talent_api.route('/<int:blogpost_id>', methods=['PUT'])
@Auth.auth_required
def update(blogpost_id):
  """
  Update A Talent
  """
  req_data = request.get_json()
  post = TalentModel.get_one_blogpost(blogpost_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = talent_schema.dump(post).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)
  
  data, error = talent_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = talent_schema.dump(post).data
  return custom_response(data, 200)

@talent_api.route('/<int:blogpost_id>', methods=['DELETE'])
@Auth.auth_required
def delete(blogpost_id):
  """
  Delete A Talent
  """
  post = TalentModel.get_one_blogpost(blogpost_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = talent_schema.dump(post).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  post.delete()
  return custom_response({'message': 'deleted'}, 204)
  

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

