from rest_service import responses

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from jeeves_commons.storage.storage import get_storage_client


class Minions(Resource):

    @swagger.operation(
        responseClass='List[{0}]'.format(responses.Minion.__name__),
        nickname="list",
        notes="Returns a list of all jeeves minions"
    )
    @marshal_with(responses.Minion.response_fields)
    def get(self, **kwargs):
        return get_storage_client().minions.list(**kwargs)
