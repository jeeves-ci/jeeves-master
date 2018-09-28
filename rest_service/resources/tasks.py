from rest_service import responses
from rest_service.resources.resource import JeevesResource
from rest_service.rest_decorators import with_params, with_storage

from flask_restful import marshal_with, marshal
from flask_restful_swagger import swagger


class Tasks(JeevesResource):

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
            order_by=None,
            page=0,
            size=100,
            storage=None,
            **kwargs):
        tsks, total = storage.tasks.list(workflow_id=workflow_id,
                                         status=status,
                                         order_by=order_by,
                                         page=0,
                                         size=size,
                                         **kwargs)
        tsks = marshal(tsks, responses.Task.response_fields)
        response = responses.Tasks(tasks=tsks,
                                   page=page,
                                   size=size,
                                   total=total)
        return response, 200, {'Access-Control-Allow-Origin': '*'}
