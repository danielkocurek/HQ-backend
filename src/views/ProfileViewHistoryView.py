#/src/views/ProfileViewHistoryView.py
from cProfile import Profile
from flask import request, Blueprint, g
from marshmallow import ValidationError

from ..shared.CustomService import custom_response
from ..shared.Authentication import Auth
from ..models.ProfileViewHistoryModel import *
from ..models.UserModel import *
from ..models.TalentModel import *
from ..models.ProfileModel import *
from ..models.CompanyModel import *

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

@profileviewhistory_api.route('/video_views_list/<int:page_num>/<int:page_length>', methods = ['GET'])
@Auth.auth_required
def get_list(page_num, page_length):
    user_id = g.user.get('id')
    try:
        userlist = ProfileViewHistoryModel.get_list_page(user_id, page_num, page_length)
    except ValidationError as error:
        print(error.messages)
        custom_response(error,400)
    data_list = profileviewhistory_schema.dump(userlist.items, many=True)
    res_data = []
    for tmp in data_list:
        if (UserModel.get_one_user(tmp.get('who')).type == 'talent'):
            try:
                data = TalentSchema().dump(TalentModel.get_talent_by_id(tmp.get('who')))
                data['type'] = 'talent'
            except ValidationError as error:
                print(error.messages)
            try:
                talent_profile = ProfileSchema().dump(ProfileModel.get_profile_by_userid(tmp.get('who')))
                data['talent_logo'] = talent_profile.get('avator')
                data['video_id'] = talent_profile.get('video_id')
                data['resume'] = talent_profile.get('resume')
            except ValidationError as error:
                print(error.messages)
            res_data.append(data)
        if (UserModel.get_one_user(tmp.get('who')).type == 'company'):
            try:
                data = CompanySchema().dump(CompanyModel.get_company_by_userid(tmp.get('who')))
                data['type'] = 'company'
            except ValidationError as error:
                print(error.messages)
            try:
                talent_profile = ProfileSchema().dump(ProfileModel.get_profile_by_userid(tmp.get('who')))
                data['company_logo'] = talent_profile.get('avator')
                data['video'] = talent_profile.get('video')
                data['resume'] = talent_profile.get('resume')
            except ValidationError as error:
                print(error.messages)
            res_data.append(data)
    return custom_response(res_data, 200)
    