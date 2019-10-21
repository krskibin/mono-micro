import os
import requests
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(os.environ['SETTINGS'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_done = db.Column(db.Boolean)
    header = db.Column(db.String(68))
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def to_dict(self):
        return {
            'id': self.id,
            'isDone': self.is_done,
            'header': self.header,
            'body': self.body,
            'timestamp': self.timestamp
        }


def auth_user(auth_header):
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify(message="Bearer token malformed.", success=False), 401

        req = requests.post('http://tokens:5000/token-decode', json={'token': auth_token})
        request_json = req.json()

        if not request_json['success']:
            return 'unauthorized'
        return request_json['user']
    return 'unauthorized'


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return jsonify(message="Welcome to task micro-service", success=True)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    auth_header = request.headers.get('Authorization')
    user_id = auth_user(auth_header)
    if not isinstance(user_id, int):
        return jsonify(message='Authentication failed', success=False)

    is_done = request.args.get('isDone', '')
    if is_done != '':
        if is_done == 'False':
            tasks_list = Task.query.filter_by(user_id=user_id, is_done=False)
        else:
            tasks_list = Task.query.filter_by(user_id=user_id, is_done=True)
    else:
        tasks_list = Task.query.filter_by(user_id=user_id)

    return jsonify(tasks=[selected_task.to_dict() for selected_task in tasks_list], success=True)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    auth_header = request.headers.get('Authorization')
    user_id = auth_user(auth_header)
    if not isinstance(user_id, int):
        return jsonify(message='Authentication failed', success=False)

    selected_task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    try:
        selected_task.to_dict()
    except AttributeError:
        return jsonify(error='Task not found', success=False), 404
    return jsonify(task=selected_task.to_dict(), success=True)


@app.route('/tasks', methods=['POST'])
def create_task():

    auth_header = request.headers.get('Authorization')
    user_id = auth_user(auth_header)
    if not isinstance(user_id, int):
        return jsonify(message='Authentication failed', success=False)

    if not request.json or not ('header' in request.json):
        return jsonify(error="Cannot create task without header", success=False), 400
    try:
        created_task = Task(
            header=request.json['header'],
            body=request.json.get('body', ''),
            is_done=False,
            user_id=user_id
        )
        db.session.add(created_task)
        db.session.commit()
    except:
        return jsonify(error="Database error", success=False), 400

    return jsonify(task=created_task.to_dict(), success=True)


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    auth_header = request.headers.get('Authorization')
    user_id = auth_user(auth_header)
    if not isinstance(user_id, int):
        return jsonify(message='Authentication failed', success=False)

    tasks_to_update = Task.query.filter_by(id=task_id, user_id=user_id).all()
    if len(tasks_to_update) == 0:
        return jsonify(error="Cannot find correct task", success=False), 404
    if not request.json:
        return jsonify(error="No json request", success=False), 404
    if 'header' in request.json and type(request.json['header']) != str:
        return jsonify(error="No header or bad header type", success=False), 400
    if 'body' in request.json and type(request.json['body']) != str:
        return jsonify(error="No body or bad body type", success=False), 400
    if 'is_done' in request.json and type(request.json['is_done']) is not bool:
        return jsonify(error="No is_done or bad done type", success=False), 400
    if 'user_id' in request.json and type(request.json['user_id']) is not int:
        return jsonify(error="No user_id or bad done type", success=False), 400
    task_to_update = tasks_to_update[0]
    task_to_update.header = request.json['header']
    task_to_update.body = request.json['body']
    task_to_update.is_done = request.json['isDone']
    try:
        db.session.commit()
    except:
        return jsonify(error="Database operational error", success=False), 400
    return jsonify(task=task_to_update.to_dict(), success=True)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    auth_header = request.headers.get('Authorization')
    user_id = auth_user(auth_header)
    if not isinstance(user_id, int):
        return jsonify(message='Authentication failed', success=False)

    try:
        task_to_delete = Task.query.filter_by(id=task_id, user_id=user_id).first()
        db.session.delete(task_to_delete)
        db.session.commit()
    except:
        return jsonify(message="Cannot deleted task " + str(task_id), sucess=False)
    return jsonify(message="Task deleted", task=task_to_delete.to_dict(), sucess=True)


@app.errorhandler(404)
def wrong_entrypoint(error):
    return jsonify(error="API entrypoint not found", success=False), 404