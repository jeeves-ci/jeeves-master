from rest_service import responses
from rest_service.rest_decorators import (with_storage,
                                          jwt_required)
from rest_service.resources.resource import JeevesResource

from flask_restful import marshal_with
from flask_restful_swagger import swagger


class Minions(JeevesResource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Minion.__name__),
        nickname="list",
        notes="Returns a list of all jeeves minions"
    )
    @with_storage
    @jwt_required
    @marshal_with(responses.Minion.response_fields)
    def get(self, storage=None, **kwargs):
        return storage.minions.list(**kwargs)
