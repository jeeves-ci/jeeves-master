from rest_service import responses
from rest_service.rest_decorators import with_storage

from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from jeeves_commons.queue import publisher


class Minion(Resource):

    @swagger.operation(
        responseClass='Minion {0}'.format(responses.Minion.__name__),
        nickname="stop",
        notes="Stop a Jeeves Minion"
    )
    @with_storage
    @marshal_with(responses.Minion.response_fields)
    def delete(self, minion_ip, storage=None, **kwargs):
        publisher.shutdown_minion(minion_ip=minion_ip)
        storage.minions.update
        return storage.minions.list(**kwargs)
