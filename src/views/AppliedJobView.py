#/src/views/AppliedJobView.py
from flask import request,Blueprint, json,g, Response
from marshmallow import ValidationError

from ..shared.CustomService import custom_response

from ..shared.Authentication import Auth
from ..models.AppliedJobModel import *
from ..models.JobModel import *
from ..models.TalentModel import *
from ..models.ProfileModel import *

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

@appliedjob_api.route('/update/<int:id>', methods=['PUT'])
@Auth.auth_required
def update(id):
    req_data = request.get_json()
    try:
        data = appliedjob_schema.load(req_data, partial=True)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error, 400)
    appliedjob = AppliedJobModel.get_one(id)
    if not data:
        return custom_response({'error':'This is not exist in applied job list'}, 400)
    appliedjob.update(data)
    return custom_response({'status':'success'},200)
        

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
        jobs = JobModel.get_all_jobs_by_pagination_allowlist(applied_job_ids, page_num, page_length)
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
        # if job_id in applied_job_ids:
        res_jobs.append(job)
    return custom_response(res_jobs, 200)

@appliedjob_api.route('/shortlist_jobs_by_user/<int:page_num>/<int:page_length>', methods = ['GET'])
@Auth.auth_required
def get_shortlist_jobs_user_by_page_num(page_num, page_length):
    user_id = g.user.get('id')
    applied_job_list = AppliedJobModel.get_shortlist_job_by_talentid(user_id)
    applied_job_ids = []
    for tmp_job in applied_job_list:
        applied_job_ids.append(AppliedJobSchema().dump(tmp_job).get('job_id'))
    try:
        jobs = JobModel.get_all_jobs_by_pagination_allowlist(applied_job_ids, page_num, page_length)
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
        # if job_id in applied_job_ids:
        res_jobs.append(job)
    return custom_response(res_jobs, 200)

@appliedjob_api.route('/jobcount_by_user', methods = ['GET'])
@Auth.auth_required
def get_jobcount_by_user():
    user_id = g.user.get('id')
    try:
        job_count = AppliedJobModel.get_jobcount_by_user(user_id)
        shortlist_job_count = AppliedJobModel.get_shortlist_jobcount_by_user(user_id)
        print(shortlist_job_count)
    except ValidationError as error:
        print(error.messages)
        return custom_response(error,400)
    return custom_response({'applied_count':job_count,'shortlist_count':shortlist_job_count, 'status':'success'}, 200)


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
        if tmp.get('shortlist_status'):
            talents_list.append(tmp.get('talent_id'))
    return custom_response({'applied_count':len(data_jobs),'shortlist_count':len(talents_list),'status':'success'}, 200)

@appliedjob_api.route('/job_by_company/<int:id>/<int:page_num>/<int:page_length>', methods = ['GET'])
@Auth.auth_required
def get_jobs_by_company(id, page_num, page_length):
    try:
        appliedjobs = AppliedJobModel.get_by_companyid_page(id, page_num, page_length)
    except ValidationError as error:
        print(error.messages)
        custom_response(error,400)
    data_jobs = appliedjob_schema.dump(appliedjobs.items, many=True)
    res_data = []
    for tmp in data_jobs:
        data = JobSchema().dump(JobModel.get_job_by_id(tmp.get('job_id')))
        data['company_logo'] = JobModel.get_companylogo(id) 
        data['company_name'] = JobModel.get_companyname(id)
        data['company_video'] = JobModel.get_companyvideo(id)
        data['appliedtalents_count'] = len(appliedjob_schema.dump(AppliedJobModel.get_by_jobid(tmp.get('job_id')), many=True))
        shortlist = []
        for ttmp in appliedjob_schema.dump(AppliedJobModel.get_by_jobid(tmp.get('job_id')), many=True):
            if ttmp.get('shortlist_status'):
                shortlist.append(ttmp.get('talent_id'))
        data['shortlisttalents_count'] = len(shortlist)
        res_data.append(data)
    return custom_response(res_data, 200)

@appliedjob_api.route('/shortlist_job_by_company/<int:id>/<int:page_num>/<int:page_length>', methods = ['GET'])
@Auth.auth_required
def get_by_shortlist_companyid_page(id, page_num, page_length):
    try:
        appliedjobs = AppliedJobModel.get_by_shortlist_companyid_page(id, page_num, page_length)
    except ValidationError as error:
        print(error.messages)
        custom_response(error,400)
    data_jobs = appliedjob_schema.dump(appliedjobs.items, many=True)
    res_data = []
    for tmp in data_jobs:
        data = JobSchema().dump(JobModel.get_job_by_id(tmp.get('job_id')))
        data['company_logo'] = JobModel.get_companylogo(id) 
        data['company_name'] = JobModel.get_companyname(id)
        data['company_video'] = JobModel.get_companyvideo(id)
        data['appliedtalents_count'] = len(appliedjob_schema.dump(AppliedJobModel.get_by_jobid(tmp.get('job_id')), many=True))
        shortlist = []
        for ttmp in appliedjob_schema.dump(AppliedJobModel.get_by_jobid(tmp.get('job_id')), many=True):
            if ttmp.get('shortlist_status'):
                shortlist.append(ttmp.get('talent_id'))
        data['shortlisttalents_count'] = len(shortlist)
        res_data.append(data)
    return custom_response(res_data, 200)

@appliedjob_api.route('/talents_by_job/<int:id>/<int:page_num>/<int:page_length>', methods = ['GET'])
@Auth.auth_required
def get_all_talents_by_job(id, page_num, page_length):
    appliedtalents = AppliedJobModel.get_by_jobid_page(id, page_num, page_length)
    data_talents = appliedjob_schema.dump(appliedtalents.items, many=True)
    res_data = []
    for tmp in data_talents:
        data = TalentSchema().dump(TalentModel.get_talent_by_userid(tmp.get('talent_id')))
        talent_profile = ProfileSchema().dump(ProfileModel.get_profile_by_userid(tmp.get('talent_id')))
        data['talent_logo'] = talent_profile.get('avator')
        data['video_id'] = talent_profile.get('video_id')
        data['resume'] = talent_profile.get('resume')
        data['is_shortlist'] = tmp.get('shortlist_status')
        data['appliedjob_id'] = tmp.get('id')
        res_data.append(data)
    return custom_response(res_data, 200)

@appliedjob_api.route('/shortlist_talents_by_job/<int:id>/<int:page_num>/<int:page_length>', methods = ['GET'])
@Auth.auth_required
def get_all_shortlist_talents_by_job(id, page_num, page_length):
    appliedtalents = AppliedJobModel.get_by_shortlist_jobid_page(id, page_num, page_length)
    data_talents = appliedjob_schema.dump(appliedtalents.items, many=True)
    res_data = []
    for tmp in data_talents:
        data = TalentSchema().dump(TalentModel.get_talent_by_userid(tmp.get('talent_id')))
        talent_profile = ProfileSchema().dump(ProfileModel.get_profile_by_userid(tmp.get('talent_id')))
        data['talent_logo'] = talent_profile.get('avator')
        data['video_id'] = talent_profile.get('video_id')
        data['resume'] = talent_profile.get('resume')
        data['is_shortlist'] = tmp.get('shortlist_status')
        data['appliedjob_id'] = tmp.get('id')
        res_data.append(data)
    return custom_response(res_data, 200)