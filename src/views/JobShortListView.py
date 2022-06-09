#/scr/views/JobShortlistView.py
from flask import request, Blueprint, Response, json
from marshmallow import ValidationError

from ..shared.CustomService import custom_response
from ..models.JobShortlistModel import *
from ..shared.Authentication import Auth
from ..models.TalentModel import *
from ..models.ProfileModel import *

jobshortlist_api = Blueprint('jobshorlist_api', __name__)
jobshortlist_schema = JobShortlistSchema()

@jobshortlist_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
        Create Jobshortlist details.
    """
    req_data = request.get_json()
    try:
        data = jobshortlist_schema.load(req_data)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error,400)
    jobshortlist = JobShortlistModel(data)
    jobshortlist.save()
    req_data = jobshortlist_schema.dump(jobshortlist)
    req_data['status'] = 'success'
    return custom_response(req_data,200)

@jobshortlist_api.route('/jobs/<int:id>', methods=['GET'])
@Auth.auth_required
def get_jobs_by_taletnid(id):
    data = JobShortlistModel.get_jobs_by_talentid(id)
    if not data:
        return custom_response({'error':'This user is not on any job shortlist' }, 400)
    res_data = []
    for jobshort in data:
        job_id = jobshortlist_schema.dump(jobshort).get('talent_id')
        res_data.append(job_id)
    return custom_response(res_data, 200)

@jobshortlist_api.route('/talents/<int:id>', methods=['GET'])
@Auth.auth_required
def get_talents_by_jobid(id):
    data = JobShortlistModel.get_talents_by_jobid(id)
    if not data:
        return custom_response({'error':'There is not any shortlisted user in this job'})
    res_data = []
    for jobshort in data:
        talent_id = jobshortlist_schema.dump(jobshort).get('job_id')
        res_data.append(talent_id)
    return custom_response(res_data, 200)

@jobshortlist_api.route('/shortlist_talents_by_job/<int:id>/<int:page_num>/<int:page_length>', methods = ['GET'])
@Auth.auth_required
def get_all_shortlist_talents_by_job(id, page_num, page_length):
    shortlisttalents = JobShortlistModel.get_by_jobid_page(id, page_num, page_length)
    data_talents = jobshortlist_schema.dump(shortlisttalents.items, many=True)
    res_data = []
    for tmp in data_talents:
        data = TalentSchema().dump(TalentModel.get_talent_by_userid(tmp.get('talent_id')))
        talent_profile = ProfileSchema().dump(ProfileModel.get_profile_by_userid(tmp.get('talent_id')))
        data['talent_logo'] = talent_profile.get('avator')
        data['video_id'] = talent_profile.get('video_id')
        data['resume'] = talent_profile.get('resume')
        res_data.append(data)
    return custom_response(res_data, 200)
