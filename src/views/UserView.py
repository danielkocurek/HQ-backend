#/src/views/UserView

from distutils.log import error
from random import randrange
from flask import request, json, Response, Blueprint, g, session
from marshmallow import ValidationError
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth
import smtplib

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

gmail_user = 'appc31058@gmail.com'
gmail_password = 'j99807jj!@#123'

@user_api.route('/', methods=['POST'])
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  try:
    data = user_schema.load(req_data)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  print(user_schema.dump(user_in_db).get('verify_code'))
  if user_in_db :
    if user_schema.dump(user_in_db).get('register_status'):
      message = {'error': 'User already exist, please supply another email address'}
      return custom_response(message, 400)
    else :
      user = UserModel(data)
      user.update(data)
      # sms_code_send(user_schema.dump(user_in_db).get('verify_code'),user_schema.dump(user_in_db).get('email') )
      return custom_response({'status': 'success'}, 200)    
    
  user = UserModel(data)
  user.save()
  ser_data = user_schema.dump(user)
  print("=======================")
  print(ser_data.get('id'))
  # token = Auth.generate_token(ser_data.get('id'))
  # print(token)
  # sms_code_send(user_schema.dump(user_in_db).get('verify_code'),user_schema.dump(user_in_db).get('email') )
  return custom_response({'status': 'success'}, 200)

@user_api.route('/verify', methods=['POST'])
def verify():
  """
  Create User Function
  """
  req_data = request.get_json()
  try:
    data = user_schema.load(req_data)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  
  # check if user already exist in the db

  user_in_db = UserModel.get_user_by_email(data.get('email'))
  update_user = user_schema.dump(user_in_db)
  print(update_user)
  # for key, item in update_user.items():
  if user_schema.dump(user_in_db).get('verify_code') != data.get('verify_code'):
    message = {'error': 'Failed Verify code, Please check code in your email'}
    return custom_response(message, 400)
  update_user['register_status'] = True
  print(update_user)

  # setattr(data, key, item)
  # user = UserModel(user_in_db)
  user_in_db.update(update_user)
  print("=======================")
  print(update_user.get('id'))
  token = Auth.generate_token(update_user.get('id'))
  # session['username'] = update_user.get('id')
  print(token)
  return custom_response({'jwt_token': token,'id':update_user.get('id'),'email':update_user.get('email'),'type':update_user.get('type'), 'status':'success'}, 200)

@user_api.route('/resend', methods=['POST'])
def resend():
  """
  Create User Function
  """
  req_data = request.get_json()
  try:
    data = user_schema.load(req_data)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  update_user = user_schema.dump(user_in_db)
  print(update_user)
  # for key, item in update_user.items():
  # if user_schema.dump(user_in_db).get('verify_code') != data.get('verify_code'):
  #   message = {'error': 'Failed Verify code, Please check code in your email'}
  #   return custom_response(message, 400)
  update_user['verify_code'] = randrange(1000,9999,4)
  user_in_db.update(update_user)
  # sms_code_send(update_user['verify_code'],update_user['email'] )
  print(update_user)

  # setattr(data, key, item)
  # user = UserModel(user_in_db)

  return custom_response({'status': 'success'}, 200)

@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  """
  Get all users
  """
  users = UserModel.get_all_users()
  ser_users = user_schema.dump(users, many=True).data
  return custom_response(ser_users, 200)

@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
  """
  Get a single user
  """
  user = UserModel.get_one_user(user_id)
  if not user:
    return custom_response({'error': 'user not found'}, 404)
  
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)

@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
  """
  Update me
  """
  req_data = request.get_json()
  data = user_schema.load(req_data, partial=True)

  user = UserModel.get_one_user(g.user.get('id'))
  user.update(data)
  ser_user = user_schema.dump(user)
  return custom_response(ser_user, 200)

@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  """
  Delete a user
  """
  user = UserModel.get_one_user(g.user.get('id'))
  user.delete()
  return custom_response({'message': 'deleted'}, 204)

@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  """
  Get me
  """
  user = UserModel.get_one_user(g.user.get('id'))
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)


@user_api.route('/login', methods=['POST'])
def login():
  """
  User Login Function
  """
  req_data = request.get_json()
  print(req_data)
  
  try:
    data = user_schema.load(req_data, partial=True)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  print(data)
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  user = UserModel.get_user_by_email(data.get('email'))
  ser_data = user_schema.dump(user)
  if not user:
    return custom_response({'error': 'invalid credentials'}, 400)
  if not user.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 400)
  if ser_data.get('register_status') != True:
    print("failed")
    return custom_response({'error':'you did not verify with sms_code'},400)
  token = Auth.generate_token(ser_data.get('id'))
  # session['username'] = ser_data.get('id')
  return custom_response({'jwt_token': token, "id":ser_data.get('id'), "email":ser_data.get('email'), "type":ser_data.get('type'), 'status':'success'}, 200)

def sms_code_send(sms_code, to_address):
  print(sms_code, to_address)
  subject = "SMS Verify"
  body = "Please check sms code to login, SMS_CODE: %s" % sms_code
  email_text = """\
  From: %s
  To: %s
  Subject: %s

  %s
  """ % (gmail_user, to_address, subject, body)
  try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(gmail_user, to_address, email_text)
    smtp_server.close()
    print("Email sent successfully!")
    return custom_response({'status':'success'},200)
  except Exception as ex:
    print("Something went wrong….",ex)  
    return custom_response(ex,400)

# @user_api.route('/logout', method=['POST'])
# @Auth.auth_required

# def logout():
#   if 'username' in session:
#     session.pop('username', None)
#   return custom_response({'status':'success'}, 200)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
