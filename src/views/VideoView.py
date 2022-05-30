#/src/views/VideoView.py
from flask import redirect, request, Blueprint, json, Response, url_for
from ..shared.Authentication import Auth
from ..models.VideoModel import *
from werkzeug.utils import secure_filename
import os

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
          file.save(os.path.join('src/static/uploads', filename))
          return custom_response({'url': url_for('static', filename='uploads/' + filename)}, 200)
  return custom_response({'url': url_for('static', filename='uploads/' + filename)}, 200)
          
@video_api.route('/display/<filename>')
# @Auth.auth_required
def display_video(filename):
  #print('display_video filename: ' + filename)
  return redirect(url_for('static', filename='uploads/' + filename), code=301)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

