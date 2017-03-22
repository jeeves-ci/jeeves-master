from rest_service import responses

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from jeeves_commons.storage.storage import get_storage_client
from jeeves_commons.queue import publisher


class Minion(Resource):

    @swagger.operation(
        responseClass='Minion {0}'.format(responses.Minion.__name__),
        nickname="stop",
        notes="Stop a Jeeves Minion"
    )
    @marshal_with(responses.Minion.response_fields)
    def delete(self, minion_ip, **kwargs):
        publisher.shutdown_minion(minion_ip=minion_ip)
        # get_storage_client().minions.update
        return get_storage_client().minions.list(**kwargs)
