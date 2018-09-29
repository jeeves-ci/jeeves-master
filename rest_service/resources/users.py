from rest_service import responses
from rest_service.resources.resource import JeevesResource
from rest_service.rest_decorators import (with_params,
                                          with_storage,
                                          jwt_required)

from flask_restful import marshal_with
from flask_restful_swagger import swagger


class Users(JeevesResource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.User.__name__),
        nickname="list",
        notes="Returns a list users."
    )
    @with_storage
    @jwt_required
    @with_params
    @marshal_with(responses.User.response_fields)
    def get(self,
            storage=None,
            user=None,
            **kwargs):
        users, total = storage.users.list(tenant_id=user.tenant_id, **kwargs)

        return users, 200, {'Access-Control-Allow-Origin': '*'}
