from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from mainAppFolder import app
from functools import wraps
import struct
from flask import request
import json
import xmltodict


def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)


def generate_auth_token(cardcode, expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 2)
    return (s.dumps({'id': str(cardcode)})).decode("utf-8")


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 2)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return True


def login_required(f):
    @wraps(f)
    def decorated_function():
        try:
            userAuth = request.headers.get('Authorization').split()
            userAuthToken = userAuth[1]
            s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 2)
            userData = s.loads(userAuthToken)
            status = userData['id']
        except:
            status = 'Warn'
        return f(status)

    return decorated_function


def convert_xml_json(string):
    jsonString = json.dumps(xmltodict.parse(string))
    reString = json.loads(jsonString)
    return reString
