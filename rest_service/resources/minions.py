from rest_service import responses
from rest_service.rest_decorators import with_storage

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger



class Minions(Resource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Minion.__name__),
        nickname="list",
        notes="Returns a list of all jeeves minions"
    )
    @with_storage
    @marshal_with(responses.Minion.response_fields)
    def get(self, storage=None, **kwargs):
        return storage.minions.list(**kwargs)
