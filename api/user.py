from flask import Blueprint, request
from data.models import addOrUpdateUser
from auth.auth_middleware import token_required

user = Blueprint('user', __name__, url_prefix='/api/v1')

@token_required
@user.route('/add_update', methods=['POST', 'PUT'])
def add_update():    
    data = request.get_json()
    addOrUpdateUser(data)
    return {
        "message": "User added/updated successfully",
        "data": None,
        "error": None
    }, 200

