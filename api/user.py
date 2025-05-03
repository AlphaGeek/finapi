from flask import Blueprint, request
from flask_cors import cross_origin
import pymongo
from data.models import addOrUpdateUser

user = Blueprint('user', __name__)

# mongo

@user.after_request
def after_request(response): 
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@user.route('/api/v1/user/add_update', methods=['POST', 'PUT'])
@cross_origin()
def addUpdateUser():    
    addOrUpdateUser(request)

