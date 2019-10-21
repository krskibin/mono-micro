import jwt
import os
import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(os.environ['SETTINGS'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class BlacklistToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return jsonify(message="Welcome to auth service micro-service", success=True)


@app.route('/token-encode', methods=['POST'])
def encode_jwt_token():
    try:
        user_id = request.json['user_id']
    except AssertionError:
        return jsonify(message='Authentication error', success=False), 400

    if type(user_id) != int:
        return jsonify(message='Authentication error', success=False), 400

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=11, seconds=0),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )
    return jsonify(token=token.decode(), success=True)


@app.route('/token-decode', methods=['POST'])
def decode_jwt_token():
    auth_token = request.json.get('token')
    if auth_token:
        try:
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return jsonify(message='Token blacklisted, please log in again', success=True)
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
            resp = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify(message='Signature expired. Please log in again.', success=False)
        except jwt.InvalidTokenError:
            return jsonify(message='Invalid token. Please log in again.', success=False)
        if not isinstance(resp, str):
            return jsonify(user=resp, success=True)
        return jsonify(message=resp, success=False)

    return jsonify(message="Token error", success=False)


@app.route('/token-blacklist', methods=['POST'])
def blacklist_jwt_token():
    auth_token = request.json.get('token')
    if auth_token:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
        resp = payload['sub']
        if not isinstance(resp, str):
            blacklist_token = BlacklistToken(token=auth_token)
            db.session.add(blacklist_token)
            db.session.commit()
            return jsonify(message="Blacklisted token", success=True)
    return jsonify(message="Cannot black tasks token", success=False)


@app.errorhandler(404)
def wrong_entrypoint(error):
    return jsonify(error="API entrypoint not found", success=False), 404
