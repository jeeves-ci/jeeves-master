
from rest_service import responses

from rest_service.rest_decorators import (with_params,
                                          with_storage,
                                          jwt_required,
                                          admin_only)
from rest_service.exceptions import (InvalidRequestBody,
                                     UserExists,
                                     UnAuthorized)
from rest_service.resources.resource import JeevesResource

from flask_restful import marshal_with, request
from flask import jsonify

from flask_jwt_extended import get_jwt_identity, jwt_optional


class User(JeevesResource):

    @with_storage
    @with_params
    @jwt_optional
    @marshal_with(responses.User.response_fields)
    def post(self, storage=None, **kwargs):
        if not request.is_json:
            raise InvalidRequestBody('Missing JSON in request')

        email = request.json.get('email', None)
        if email is None:
            raise InvalidRequestBody('Email is required')

        user = storage.users.get(email=email)
        if user is not None:
            raise UserExists('User with email {} already exists'.
                             format(email))

        password = request.json.get('password', None)
        if password is None:
            raise InvalidRequestBody('Password is required')

        jwt_user = get_jwt_identity()
        if jwt_user is None:
            org = request.json.get('organization', None)
            if org is None:
                raise InvalidRequestBody('Expecting organization name')
            tenant = storage.tenants.get(name=org)
            if tenant is not None:
                raise InvalidRequestBody('Organization already exists')
            tenant = storage.tenants.create(name=org)
            user = storage.users.create(email=email,
                                        password=password,
                                        role='Administrator',
                                        tenant_id=tenant.id)
        else:
            current_user = storage.users.get(email=jwt_user)
            if current_user.role != 'Administrator':
                raise UnAuthorized('User {0} is not authorized to create users'
                                   .format(email))
            role = request.json.get('role', None)
            if role is None:
                raise InvalidRequestBody('role is required')
            if role not in ['Administrator', 'Editor', 'Viewer']:
                raise InvalidRequestBody('role should be either '
                                         'Administrator/Editor/Viewer')

            user = storage.users.create(email=email,
                                        password=password,
                                        role=role,
                                        tenant_id=current_user.tenant_id)

        return user, 200, {'Access-Control-Allow-Origin': '*'}

    @with_storage
    @jwt_required
    @admin_only
    @with_params
    def delete(self, **kwargs):
        # implement
        return jsonify({}), 200, {'Access-Control-Allow-Origin': '*'}
