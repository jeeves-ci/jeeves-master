from rest_service import responses

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from rest_service.storage import get_storage_client
from rest_service.rest_decorators import with_params


class Workflows(Resource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Workflow.__name__),
        nickname="list",
        notes="Returns a list of tasks served to jeeves."
    )
    @with_params
    @marshal_with(responses.Workflow.response_fields)
    def get(self, status=None, **kwargs):
        return get_storage_client().workflows.list(status=status), 200, \
               {'Access-Control-Allow-Origin': '*'}
