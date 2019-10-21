import os
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(os.environ['SETTINGS'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@app.route('/')
@app.route('/index')
def index():
    return jsonify(message="Welcome to users api", success=True)


@app.route('/users', methods=['GET'])
def get_user():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify(message="Bearer token malformed.", success=False), 401

        req = requests.post('http://tokens:5000/token-decode', json={'token': auth_token})
        request_json = req.json()
        if request_json.get('success', False):
            response_user_id = request_json.get('user', None)
            if not response_user_id:
                return jsonify(message="Authentication error"), 404
            u = User.query.filter_by(id=response_user_id).first()
            user = {
                'username': u.username,
                'email': u.email,
            }
            print('logged in')
            return jsonify(user=user, success=True)
    return jsonify(message="Authentication error"), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify(message='must include username, email and password fields'), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify(message='please use a different username'), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify(message='please use a different email address'), 400
    user = User(
        username=data['username'],
        email=data['email']
    )

    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    req = requests.post('http://tokens:5000/token-encode', json={'user_id': user.id})
    token = req.json()['token']

    if not token:
        return jsonify(message="Cannot create user token", success=False)
    user_dict = {
        'username': user.username,
        'email': user.email,
        'id': user.id
    }
    response = jsonify(user=user_dict, authToken=token, success=True)
    return response


@app.route('/login', methods=['POST'])
def login_user():
    data = request.json or {}
    print(data)
    if 'username' not in data or 'password' not in data:
        return jsonify(message='must include username, email and password fields'), 400

    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        req = requests.post('http://tokens:5000/token-encode', json={'user_id': user.id})
        token = req.json()['token']

        if not token:
            return jsonify(message="Cannot create user token", success=False)
        user_dict = {
            'username': user.username,
            'email': user.email,
            'id': user.id
        }
        return jsonify(user=user_dict, authToken=token, success=False)

    return jsonify(message="Cannot create user", success=False)


@app.route('/logout', methods=['POST'])
def user_logout():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify(message="Bearer token malformed.", success=False), 401

        req = requests.post('http://tokens:5000/token-blacklist', json={'token': auth_token})
        request_json = req.json()

        if request_json['success']:
            return jsonify(message="Successfully logged out", success=True)

    return jsonify(message="Something goes wrong :(, not logged out", success=False)


@app.errorhandler(404)
def wrong_entrypoint(error):
    return jsonify(error="API entrypoint not found", success=False), 404