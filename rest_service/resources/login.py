import hashlib

from rest_service import responses
from rest_service.exceptions import InvalidRequestBody, UnAuthorized
from rest_service.resources.resource import JeevesResource
from rest_service.rest_decorators import with_storage

from flask_restful import marshal_with, request
from flask_restful_swagger import swagger
from flask_jwt_extended import create_access_token


class Login(JeevesResource):

    @swagger.operation(
        responseClass='{0}'.format(responses.User.__name__),
        nickname="get",
        notes="Returns a jwt token to be used for request authorization"
    )
    @with_storage
    @marshal_with(responses.Authentication.response_fields)
    def post(self, storage, **kwargs):
        if not request.is_json:
            raise InvalidRequestBody('Missing JSON in request')

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email:
            raise InvalidRequestBody('Missing email parameter')
        if not password:
            raise InvalidRequestBody('Missing password parameter')

        user = storage.users.get(email=email)
        if user is None:
            raise UnAuthorized('Bad email or password')

        hashed_password = hashlib.sha512(password + user.salt).hexdigest()

        if user.password != hashed_password:
            raise UnAuthorized('Bad email or password')

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=email)
        return ({'access_token': access_token},
                200,
                {'Access-Control-Allow-Origin': '*'})
