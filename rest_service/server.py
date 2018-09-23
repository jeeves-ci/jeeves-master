import os

from flask import Flask, jsonify
from flask_restful import Api

from rest_service import config
from rest_service.resources.tasks import Tasks
from rest_service.resources.workflows import Workflows
from rest_service.resources.workflow import Workflow
from rest_service.resources.task import Task
from rest_service.exceptions import JeevesServerError
from web_ui.web_server import LogStreamHttpServer

from jeeves_commons.storage.database import init_db
from sqlalchemy import create_engine # noqa

from jeeves_commons.constants import (DEFAULT_REST_PORT,
                                      MASTER_HOST_PORT_ENV,
                                      RABBITMQ_HOST_IP_ENV,
                                      RABBITMQ_HOST_PORT_ENV,
                                      MINION_TASKS_QUEUE,
                                      DEFAULT_BROKER_PORT,
                                      DEFAULT_WEBUI_PORT)
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


app = JeevesFlask()


@app.errorhandler(JeevesServerError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app.api.add_resource(Workflow,
                     '/api/v1.0/workflow',
                     endpoint='api/v1.0/workflow',
                     defaults={'workflow_id': None,
                               'execute': True})
app.api.add_resource(Workflows,
                     '/api/v1.0/workflows',
                     endpoint='api/v1.0/workflows',
                     defaults={'status': None,
                               'order_by': None,
                               'page': 1,
                               'size': 10})

app.api.add_resource(Task,
                     '/api/v1.0/task',
                     endpoint='/api/v1.0/task',
                     defaults={'task_id': None})
app.api.add_resource(Tasks,
                     '/api/v1.0/tasks',
                     endpoint='api/v1.0/tasks',
                     defaults={'workflow_id': None,
                               'status': None,
                               'order_by': None,
                               'page': 1,
                               'size': 100}
                     )

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
