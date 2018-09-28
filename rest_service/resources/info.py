from rest_service import responses
from rest_service.resources.resource import JeevesResource

from flask_restful import marshal_with
from flask_restful_swagger import swagger

from flask_jwt_extended import jwt_required


class Info(JeevesResource):

    @swagger.operation(
        responseClass='{0}'.format(responses.Info.__name__),
        nickname="get",
        notes="Returns server info"
    )
    @jwt_required
    @marshal_with(responses.Info.response_fields)
    def get(self, task_id=None, **kwargs):
        return {'task_id': task_id}, 200, {'Access-Control-Allow-Origin': '*'}

    def options(self):
        return None, 200, {'Access-Control-Allow-Origin': '*',
                           'Allow': 'GET',
                           "Access-Control-Allow-Headers": "Content-Type"}
