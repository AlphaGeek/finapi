from functools import wraps
import jwt
from flask import request
from flask import current_app as app
from data.models import addOrUpdateUser 
from google.oauth2 import id_token
from google.auth.transport import requests

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            print(data)
            current_user = addOrUpdateUser(data)
            
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated

def verify_id(idToken):
    try:
        idinfo = id_token.verify_oauth2_token(
            idToken, requests.Request(), CLIENT_ID
        )
        userid = idinfo['sub']
        return userid
    except ValueError:
        return null
