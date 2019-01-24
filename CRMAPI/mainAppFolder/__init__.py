from flask import Flask
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'trantrongtyckiuzk4ever!@#!!!@@##!*&%^$$#$'
app.config['SqlState'] = True
from mainAppFolder.crmapi.views import crmapiApp
app.register_blueprint(crmapiApp)