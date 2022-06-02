#/src/views/VideoView.py
from flask import g, redirect, request, Blueprint, json, Response, url_for
from marshmallow import ValidationError
from ..shared.CustomService import custom_response
from ..shared.Authentication import Auth
from ..models.VideoModel import *
from werkzeug.utils import secure_filename
import os
import datetime
video_api = Blueprint('video_api', __name__)
video_schema = VideoSchema()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@video_api.route('/file', methods=['POST'])
@Auth.auth_required
def upload_file():
  print(request.method) 
  if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
          return custom_response({'error': "this is not file "}, 400)
      file = request.files['file']
      print(file.filename)
      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
          return custom_response({'error': "this is not allowed file "}, 400)
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          print(os.path.join('src/static/uploads', filename))
          ts = datetime.datetime.now().timestamp()
          file.save(os.path.join('src/static/uploads',  str(g.user.get('id')) + '_' + str(ts).split('.')[0] + "_" + filename))
          return custom_response({'url': url_for('static', filename='uploads/' + str(g.user.get('id')) + '_' + str(ts).split('.')[0] + "_" + filename), 'status':'success'}, 200)
  return custom_response({'url': url_for('static', str(g.user.get('id')) + '_' + str(ts).split('.')[0] + "_" + filename), 'status':'success'}, 200)

@video_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  req_data = request.get_json()
  try:
    data = video_schema.load(req_data)
  except ValidationError as error:
    print(error.messages)
    return custom_response(error,400)
  video = VideoModel(data)
  video.save()
  res_data = video_schema.dump(video)
  res_data['status'] = 'success'
  return custom_response(res_data,200)

@video_api.route('/update/<int:id>',methods=['PUT'])
@Auth.auth_required
def update(id):
  req_data = request.get_json()
  data = video_schema.load(req_data)
  video = VideoModel.get_video(id)
  video.update(data)
  res_video = video_schema.dump(video)
  res_video['status'] = 'success'
  return custom_response(res_video,200)



          
@video_api.route('/display/<filename>')
# @Auth.auth_required
def display_video(filename):
  #print('display_video filename: ' + filename)
  return redirect(url_for('static', filename='uploads/' + filename), code=301)


