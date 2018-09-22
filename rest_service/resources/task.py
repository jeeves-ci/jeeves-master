from rest_service import responses
from rest_service.rest_decorators import with_storage

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger


class Task(Resource):

    @swagger.operation(
        responseClass='{0}'.format(responses.Task.__name__),
        nickname="get",
        notes="Returns a task by it's ID"
    )
    @with_storage
    @marshal_with(responses.Task.response_fields)
    def get(self, task_id=None, storage=None, **kwargs):
        return storage.tasks.get(task_id=task_id, **kwargs)
