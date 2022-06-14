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

# @profileviewhistory_api.route('/list_by_company/<int:id>/<int:page_num>/<int:page_length>', methods = ['GET'])
# @Auth.auth_required
# def get_jobs_by_company(id, page_num, page_length):
#     try:
#         appliedjobs = ProfileViewHistoryModel.get_by_companyid_page(id, page_num, page_length)
#     except ValidationError as error:
#         print(error.messages)
#         custom_response(error,400)
#     data_jobs = appliedjob_schema.dump(appliedjobs.items, many=True)
#     res_data = []
#     for tmp in data_jobs:
#         data = JobSchema().dump(JobModel.get_job_by_id(tmp.get('job_id')))
#         data['company_logo'] = JobModel.get_companylogo(id) 
#         data['company_name'] = JobModel.get_companyname(id)
#         data['company_video'] = JobModel.get_companyvideo(id)
#         data['appliedtalents_count'] = len(appliedjob_schema.dump(AppliedJobModel.get_by_jobid(tmp.get('job_id')), many=True))
#         shortlist = []
#         for ttmp in appliedjob_schema.dump(AppliedJobModel.get_by_jobid(tmp.get('job_id')), many=True):
#             if ttmp.get('shortlist_status'):
#                 shortlist.append(ttmp.get('talent_id'))
#         data['shortlisttalents_count'] = len(shortlist)
#         res_data.append(data)
#     return custom_response(res_data, 200)
    