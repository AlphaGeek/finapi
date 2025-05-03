from flask import Flask, request, Response
from flask_cors import CORS 
from api.market_data import earnings, search, timeSeries
from api.user import user
from api.ai import open_ai
import os

app = Flask(__name__)
SECRET_KEY = os.environ.get('GOOGLE_SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

app.register_blueprint(user)
app.register_blueprint(earnings)
app.register_blueprint(timeSeries)
app.register_blueprint(search)
app.register_blueprint(open_ai)

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route('/')
def index():
    return ""
