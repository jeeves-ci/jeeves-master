from rest_service import responses
from rest_service.rest_decorators import with_params

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from jeeves_commons.storage.storage import get_storage_client


class Tasks(Resource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Task.__name__),
        nickname="list",
        notes="Returns a list of tasks served to jeeves."
    )
    @with_params
    @marshal_with(responses.Task.response_fields)
    def get(self, workflow_id=None, status=None, **kwargs):
        return get_storage_client().tasks.list(workflow_id=workflow_id,
                                               status=status,
                                               **kwargs), \
               200, \
               {'Access-Control-Allow-Origin': '*'}
