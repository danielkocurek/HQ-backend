#/src/views/AppliedJobView.py
from flask import request,Blueprint, json, Response
from marshmallow import ValidationError

from ..shared.CustomService import custom_response

from ..shared.Authentication import Auth
from ..models.AppliedJobModel import *

appliedjob_api = Blueprint('appliedjob_api', __name__)
appliedjob_schema = AppliedJobSchema()

@appliedjob_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
        Create appliedjob details
    """
    req_data = request.get_json()
    try:
        data = appliedjob_schema.load(req_data)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error, 400)
    appliedjob = AppliedJobModel(data)
    appliedjob.save()
    res_data = appliedjob_schema.dump(appliedjob)
    res_data['status'] = 'success'
    return custom_response(res_data,200)

@appliedjob_api.route('/jobs/<int:id>', methods=['GET'])
@Auth.auth_required
def get_jobs_by_talentid(id):
    data = AppliedJobModel.get_jobs_by_talentid(id)
    if not data:
        return custom_response({'error':'This user did not bid any jobs'}, 400)
    res_data = []
    for appliedjob in data:
        job_id = appliedjob_schema.load(appliedjob).get('job_id')
        res_data.append(job_id)
    return custom_response(res_data,200)

@appliedjob_api.route('/talents/<int:id>', methods=['GET'])
@Auth.auth_required
def get_talents_by_jobid(id):
    data = AppliedJobModel.get_talents_by_jobid(id)
    if not data:
        return custom_response({'error':'Any talents did not apply this job'}, 400)
    res_data = []
    for appliedjob in data:
        talent_id = appliedjob_schema.load(appliedjob)
        res_data.append(talent_id)
    return custom_response(res_data,200)
    
        
    

    