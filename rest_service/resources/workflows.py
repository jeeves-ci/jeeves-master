from rest_service import responses
from rest_service.resources.resource import JeevesResource

from flask_restful import marshal_with, marshal
from flask_restful_swagger import swagger

from rest_service.rest_decorators import with_params, with_storage


class Workflows(JeevesResource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Workflows.__name__),
        nickname="list",
        notes="Returns a list of workflows served to jeeves."
    )
    @with_storage
    @with_params
    @marshal_with(responses.Workflows.response_fields)
    def get(self,
            status=None,
            page=0,
            size=10,
            order_by=None,
            pattern=None,
            storage=None,
            **kwargs):
        # raise UnAuthorized('You are NOT authorized')
        wfs, total = storage.workflows.list(status=status,
                                            order_by=order_by,
                                            pattern=pattern,
                                            page=page,
                                            size=size,
                                            **kwargs)
        wfs = marshal(wfs, responses.Workflow.response_fields)
        response = responses.Workflows(workflows=wfs,
                                       page=page,
                                       size=size,
                                       total=total)
        return response, 200, {'Access-Control-Allow-Origin': '*'}
