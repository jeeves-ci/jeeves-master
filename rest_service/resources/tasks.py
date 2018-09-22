from rest_service import responses
from rest_service.rest_decorators import with_params, with_storage

from flask_restful import Resource, marshal_with, marshal
from flask_restful_swagger import swagger

from rest_service.storage import storage_client


class Tasks(Resource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Task.__name__),
        nickname="list",
        notes="Returns a list of tasks served to jeeves."
    )
    @with_storage
    @with_params
    @marshal_with(responses.Tasks.response_fields)
    def get(self,
            workflow_id=None,
            status=None,
            page=1,
            size=100,
            storage=None,
            **kwargs):
        tsks, total = storage.tasks.list(workflow_id=workflow_id,
                                         status=status,
                                         page=page,
                                         size=size,
                                         **kwargs)
        tsks = marshal(tsks, responses.Task.response_fields)
        response = responses.Tasks(tasks=tsks,
                                   page=page,
                                   size=size,
                                   total=total)
        return response, 200, {'Access-Control-Allow-Origin': '*'}
