from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class Task(object):
    def __init__(self, **kwargs):
        self.workflow_id = kwargs.get('workflow_id')
        self.minion_ip = kwargs.get('minion_ip')
        self.task_id = kwargs.get('task_id')
        self.task_name = kwargs.get('task_name')
        self.status = kwargs.get('status')
        self.content = kwargs.get('content')
        self.created_at = kwargs.get('created_at')
        self.started_at = kwargs.get('started_at')
        self.date_done = kwargs.get('date_done')
        # self.result = kwargs.get('result')
        self.traceback = kwargs.get('traceback')

    response_fields = {
        'task_id': fields.String,
        'task_name': fields.String,
        'status': fields.String,
        'content': fields.String,
        'workflow_id': fields.String,
        'minion_ip': fields.String,
        'created_at': fields.String,
        'started_at': fields.String,
        'date_done': fields.String,
        # 'result': fields.String,
        'traceback': fields.String,
    }


@swagger.model
class Minion(object):
    def __init__(self, **kwargs):
        self.minion_id = kwargs.get('minion_id')
        self.minion_ip = kwargs.get('minion_ip')
        self.status = kwargs.get('status')
        self.started_at = kwargs.get('started_at')

    response_fields = {
        'minion_id': fields.String,
        'minion_ip': fields.String,
        'status': fields.String,
        'started_at': fields.String,
    }


@swagger.model
class Workflow(object):
    def __init__(self, **kwargs):
        self.status = kwargs.get('status')
        self.workflow_id = kwargs.get('workflow_id')
        self.started_at = kwargs.get('started_at')
        self.ended_at = kwargs.get('ended_at')

    response_fields = {
        'name': fields.String,
        'status': fields.String,
        'workflow_id': fields.String,
        'started_at': fields.String,
        'ended_at': fields.String,
    }


@swagger.model
class Workflows(object):
    def __init__(self, **kwargs):
        self.workflows = kwargs.get('workflows')
        self.page = kwargs.get('page')
        self.size = kwargs.get('size')
        self.total = kwargs.get('total')

    response_fields = {
        'workflows': fields.Raw,
        'page': fields.Integer,
        'size': fields.Integer,
        'total': fields.Integer,
    }


@swagger.model
class Tasks(object):
    def __init__(self, **kwargs):
        self.tasks = kwargs.get('tasks')
        self.page = kwargs.get('page')
        self.size = kwargs.get('size')
        self.total = kwargs.get('total')

    response_fields = {
        'tasks': fields.Raw,
        'page': fields.Integer,
        'size': fields.Integer,
        'total': fields.Integer,
    }


@swagger.model
class User(object):
    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.role = kwargs.get('role')

    response_fields = {
        'email': fields.String,
        'role': fields.String,
    }


@swagger.model
class Authentication(object):
    def __init__(self, **kwargs):
        self.access_token = kwargs.get('access_token')

    response_fields = {
        'access_token': fields.String,
    }


@swagger.model
class Info(object):
    def __init__(self, **kwargs):
        self.version = kwargs.get('version')

    response_fields = {
        'version': fields.String,
    }
