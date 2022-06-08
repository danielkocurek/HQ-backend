#/src/views/AppliedJobView.py
from flask import request,Blueprint, json,g, Response
from marshmallow import ValidationError

from ..shared.CustomService import custom_response

from ..shared.Authentication import Auth
from ..models.AppliedJobModel import *
from ..models.JobModel import *

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
    data = AppliedJobModel.get_by_talentid(id)
    print(data)
    if not data:
        return custom_response({'error':'This user did not bid any jobs'}, 400)
    res_data = []
    for appliedjob in data:
        job_id = appliedjob_schema.dump(appliedjob).get('job_id')
        res_data.append(job_id)
    return custom_response(res_data,200)

@appliedjob_api.route('/jobs_by_companyid/<int:id>', methods=['GET'])
@Auth.auth_required
def get_jobs_by_companyid(id):
    data = AppliedJobModel.get_by_companyid(id)
    if not data:
        return custom_response({'error':'This user did not bid any jobs'}, 400)
    res_data = []
    for appliedjob in data:
        job_id = appliedjob_schema.dump(appliedjob).get('job_id')
        res_data.append(job_id)
    return custom_response(res_data,200)

@appliedjob_api.route('/talents/<int:id>', methods=['GET'])
@Auth.auth_required
def get_talents_by_jobid(id):
    data = AppliedJobModel.get_by_jobid(id)
    if not data:
        return custom_response({'error':'Any talents did not apply this job'}, 400)
    res_data = []
    for appliedjob in data:
        talent_id = appliedjob_schema.dump(appliedjob)
        res_data.append(talent_id)
    return custom_response(res_data,200)

@appliedjob_api.route('/jobs_by_user/<int:page_num>/<int:page_length>', methods = ['GET'])
@Auth.auth_required
def get_jobs_user_by_page_num(page_num, page_length):
    user_id = g.user.get('id')
    applied_job_list = AppliedJobModel.get_by_talentid(user_id)
    applied_job_ids = []
    for tmp_job in applied_job_list:
        applied_job_ids.append(AppliedJobSchema().dump(tmp_job).get('job_id'))
    try:
        jobs = JobModel.get_all_jobs_by_pagination(page_num, page_length)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error,400)
    if not jobs:
        return custom_response({'error':'This company did not post any jobs'},400)
    data_jobs = JobSchema().dump(jobs.items, many=True)
    res_jobs = []
    for job in data_jobs:
        company_id = job.get('company_id')
        job_id = job.get('id')
        job['company_logo'] = JobModel.get_companylogo(company_id)
        job['company_name'] = JobModel.get_companyname(company_id)
        job['company_video'] = JobModel.get_companyvideo(company_id)
        if job_id in applied_job_ids:
            res_jobs.append(job)
    return custom_response(res_jobs, 200)

@appliedjob_api.route('/jobcount_by_user', methods = ['GET'])
@Auth.auth_required
def get_jobcount_by_user():
    user_id = g.user.get('id')
    try:
        job_count = AppliedJobModel.get_jobcount_by_user(user_id)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error,400)
    return custom_response({'count':job_count,'status':'success'}, 200)


@appliedjob_api.route('/talentcount_by_company/<int:id>', methods = ['GET'])
@Auth.auth_required
def get_talentcount_by_company(id):
    try:
        appliedjobs = AppliedJobModel.get_by_companyid(id)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error,400)
    data_jobs = appliedjob_schema.dump(appliedjobs, many=True)
    talents_list = []
    for tmp in data_jobs:
        talents_list.append(tmp.get('talent_id'))
    # talents_list = list(set(talents_list))
    print(len(talents_list))
    return custom_response({'count':len(talents_list),'status':'success'}, 200)
    
    
        
    

    