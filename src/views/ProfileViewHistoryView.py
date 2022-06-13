#/src/views/ProfileViewHistoryView.py
from cProfile import Profile
from flask import request, Blueprint
from marshmallow import ValidationError

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
    