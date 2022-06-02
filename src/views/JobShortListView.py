#/scr/views/JobShortlistView.py
from flask import request, Blueprint, Response, json
from marshmallow import ValidationError

from ..shared.CustomService import custom_response
from ..models.JobShortlistModel import *
from ..shared.Authentication import Auth

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
        job_id = jobshortlist_schema.load(jobshort).get('talent_id')
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
        talent_id = jobshortlist_schema.load(jobshort).get('job_id')
        res_data.append(talent_id)
    return custom_response(res_data, 200)
