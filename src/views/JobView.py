#/src/views/JobView.py
from flask import request, g, Blueprint, json, Response

from ..shared.Authentication import Auth
from ..models.JobModel import *

job_api = Blueprint('job_api', __name__)
job_schema = JobSchema()

@job_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
        Create Job Details
    """
    req_data = request.get_json()
    data = job_schema.load(req_data)
    
    job = JobModel(data)
    job.save()
    data = job_schema.dump(job)
    data['status'] = 'success'
    return custom_response(data, 200)

@job_api.route('/update/<int:id>', methods=['PUT'])
@Auth.auth_required
def update(id):
    """
        Update Job Details
    Returns:
        Updated job details
    """
    req_data = request.get_json()
    data = job_schema.load(req_data)
    
    job = JobModel.get_job_by_id(id)
    job.update(data)
    
    res_job = job_schema.dump(job)
    res_job['status'] = 'success'
    return custom_response(res_job, 200)

@job_api.route('/<int:id>', methods = ['GET'])
@Auth.auth_required
def get_job(id):
    job = JobModel.get_job_by_id(id)
    if not job:
        return custom_response({'error':'This job does not exist'},200)
    res_job = job_schema.dump(job)
    res_job['status'] = 'success'
    return custom_response(res_job, 200)

@job_api.route('/all/<int:id>', methods = ['GET'])
@Auth.auth_required
def get_jobs_by_companyid(id):
    jobs = JobModel.get_all_job_by_companyid(id)
    if not jobs:
        return custom_response({'error':'This company did not post any jobs'},400)
    res_jobs = job_schema.dump(jobs, many=True)
    # res_job = job_schema.dump(job)
    # res_job['status'] = 'success'
    return custom_response(res_jobs, 200)


@job_api.route('/all', methods = ['GET'])
@Auth.auth_required
def get_all_jobs():
    jobs = JobModel.get_all_jobs()
    if not jobs:
        return custom_response({'error':'Companies did not post any jobs'},400)
    res_jobs = job_schema.dump(jobs, many=True)
    # res_job = job_schema.dump(job)
    # res_job['status'] = 'success'
    return custom_response(res_jobs, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
  )