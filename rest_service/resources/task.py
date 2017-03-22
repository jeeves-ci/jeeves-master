from rest_service import responses

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from jeeves_commons.storage.storage import get_storage_client


class Task(Resource):

    @swagger.operation(
        responseClass='{0}'.format(responses.Task.__name__),
        nickname="get",
        notes="Returns a task by it's ID"
    )
    @marshal_with(responses.Task.response_fields)
    def get(self, task_id=None, **kwargs):
        return get_storage_client().tasks.get(task_id=task_id,
                                              **kwargs)
