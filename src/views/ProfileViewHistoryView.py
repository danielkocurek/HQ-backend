#/src/views/ProfileViewHistoryView.py
from cProfile import Profile
from flask import request, Blueprint, g
from marshmallow import ValidationError

from src.models.CompanyModel import CompanyModel

from ..shared.CustomService import custom_response
from ..shared.Authentication import Auth
from ..models.ProfileViewHistoryModel import *

profileviewhistory_api = Blueprint('profileviewhistory_api', __name__)
profileviewhistory_schema = ProfileViewHistorySchema()

@profileviewhistory_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    try:
        data = profileviewhistory_schema.load(req_data)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error, 400)
    history = ProfileViewHistoryModel(data)
    history.save()
    res_data = profileviewhistory_schema.dump(history)
    res_data['status'] = 'success'
    return custom_response(res_data, 200)

@profileviewhistory_api.route('/company', methods=['POST'])
@Auth.auth_required
def company_create():
    req_data = request.get_json()
    req_data['which'] = CompanyModel.get_company_by_id(req_data['which']).user_id
    try:
        data = profileviewhistory_schema.load(req_data)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error, 400)
    history = ProfileViewHistoryModel(data)
    history.save()
    res_data = profileviewhistory_schema.dump(history)
    res_data['status'] = 'success'
    return custom_response(res_data, 200)

@profileviewhistory_api.route('/', methods=['GET'])
@Auth.auth_required
def get_video_counts_by_userid():
    user_id = g.user.get('id')
    print(user_id)
    count = ProfileViewHistoryModel.get_all_count(user_id) 
    res_data = {}
    res_data['count'] = count
    res_data['status'] = 'success'
    return custom_response(res_data, 200)   
    