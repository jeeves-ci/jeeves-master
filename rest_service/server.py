import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from rest_service import config
from rest_service.resources.login import Login
from rest_service.resources.user import User
from rest_service.resources.users import Users
from rest_service.resources.tasks import Tasks
from rest_service.resources.workflows import Workflows
from rest_service.resources.workflow import Workflow
from rest_service.resources.task import Task
from rest_service.resources.info import Info
from rest_service.exceptions import JeevesServerError
from web_ui.web_server import LogStreamHttpServer

from jeeves_commons.storage.database import init_db
from jeeves_commons.storage.storage import get_storage_client as get_storage
from sqlalchemy import create_engine # noqa

from jeeves_commons.constants import (DEFAULT_REST_PORT,
                                      MASTER_HOST_PORT_ENV,
                                      RABBITMQ_HOST_IP_ENV,
                                      RABBITMQ_HOST_PORT_ENV,
                                      JEEVES_JWT_SECRET_KEY_ENV,
                                      JEEVES_ADMIN_EMAIL_ENV,
                                      JEEVES_ADMIN_PASSWORD_ENV,
                                      JEEVES_ORG_NAME_ENV,
                                      MINION_TASKS_QUEUE,
                                      DEFAULT_BROKER_PORT,
                                      DEFAULT_WEBUI_PORT,
                                      DEFAULT_JEEVES_JWT_SECRET_KEY,
                                      DEFAULT_JEEVES_ADMIN_EMAIL,
                                      DEFAULT_JEEVES_ADMIN_PASSWORD,
                                      DEFAULT_JEEVES_ORG_NAME)
from jeeves_commons.utils import open_channel


REST_PORT = int(os.environ.get(MASTER_HOST_PORT_ENV, DEFAULT_REST_PORT))
MESSAGE_BROKER_HOST_IP = os.getenv(RABBITMQ_HOST_IP_ENV, '172.17.0.3')
MESSAGE_BROKER_HOST_PORT = os.getenv(RABBITMQ_HOST_PORT_ENV,
                                     DEFAULT_BROKER_PORT)


class JeevesFlask(Flask):

    def __init__(self):
        super(JeevesFlask, self).__init__(__name__)
        config.instance.load_conf()
        self._init_sql_alchemy()
        self.api = Api(self)

    @staticmethod
    def _init_sql_alchemy():
        init_db()
        storage = get_storage()
        admin_email = os.getenv(JEEVES_ADMIN_EMAIL_ENV,
                                DEFAULT_JEEVES_ADMIN_EMAIL)

        default_tenant = os.getenv(JEEVES_ORG_NAME_ENV,
                                   DEFAULT_JEEVES_ORG_NAME)
        tenant = storage.tenants.get(name=default_tenant)
        if tenant is None:
            tenant = storage.tenants.create(name=default_tenant)
        if storage.users.get(email=admin_email) is None:
            admin_password = os.getenv(JEEVES_ADMIN_PASSWORD_ENV,
                                       DEFAULT_JEEVES_ADMIN_PASSWORD)
            storage.users.create(email=admin_email,
                                 password=admin_password,
                                 role='Administrator',
                                 tenant_id=tenant.id)
        storage.commit()
        storage.close()


app = JeevesFlask()

app.config['TRAP_HTTP_EXCEPTIONS'] = True


@app.errorhandler(JeevesServerError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app.api.add_resource(Login,
                     '/api/v1.0/login',
                     endpoint='api/v1.0/login')

app.api.add_resource(Info,
                     '/api/v1.0/info',
                     endpoint='api/v1.0/info')

app.api.add_resource(User,
                     '/api/v1.0/user',
                     endpoint='api/v1.0/user')

app.api.add_resource(Users,
                     '/api/v1.0/users',
                     endpoint='api/v1.0/users')

app.api.add_resource(Workflow,
                     '/api/v1.0/workflow',
                     endpoint='api/v1.0/workflow',
                     defaults={'name': None,
                               'execute': True})
app.api.add_resource(Tasks,
                     '/api/v1.0/workflow/<workflow_id>/tasks',
                     endpoint='/api/v1.0/workflow/<workflow_id>/tasks',
                     defaults={'status': None,
                               'order_by': None,
                               'page': 1,
                               'size': 100})
app.api.add_resource(
                 Task,
                 '/api/v1.0/workflow/<workflow_id>/task/<task_id>',
                 endpoint='/api/v1.0/workflow/<workflow_id>/task/<task_id>')

app.api.add_resource(Workflows,
                     '/api/v1.0/workflows',
                     endpoint='api/v1.0/workflows',
                     defaults={'status': None,
                               'order_by': None,
                               'pattern': None,
                               'page': 1,
                               'size': 10})


app.config['JWT_SECRET_KEY'] = os.getenv(JEEVES_JWT_SECRET_KEY_ENV,
                                         DEFAULT_JEEVES_JWT_SECRET_KEY)
jwt = JWTManager(app)
# app.api.add_resource(Minion,
#                      '/api/v1.0/minion/<minion_ip>',
#                      '/api/v1.0/minion/<minion_ip>')
# app.api.add_resource(Minions,
#                      '/api/v1.0/minions',
#                      '/api/v1.0/minions')
app.api.init_app(app)


class ServerBootstrapper(object):
    def __init__(self):
        # Create the minions queue
        self._create_queue()

    def _create_queue(self):
        with open_channel(MESSAGE_BROKER_HOST_IP,
                          MESSAGE_BROKER_HOST_PORT) as _channel:
            _channel.queue_declare(queue=MINION_TASKS_QUEUE,
                                   durable=True)

    def start(self):
        global app
        # Start Web-UI.
        # TODO: This needs to be ran as a separate process.
        web_ui = LogStreamHttpServer()
        web_ui.start(DEFAULT_WEBUI_PORT)

        # Start RESTful service
        app.run(host='0.0.0.0', port=REST_PORT)


if __name__ == '__main__':
    sb = ServerBootstrapper()
    sb.start()
