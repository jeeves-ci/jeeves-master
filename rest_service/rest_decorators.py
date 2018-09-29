from rest_service.storage import storage_client
from rest_service.exceptions import UnAuthorized

from flask_restful import reqparse
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def with_params(func):
    def inject_params(*args, **kwargs):
        parser = reqparse.RequestParser()
        for arg in kwargs.keys():
            parser.add_argument(arg)
        url_args = parser.parse_args()
        for arg in kwargs.keys():
            if not url_args.get(arg):
                url_args[arg] = kwargs.get(arg)
        return func(*args, **url_args)
    return inject_params


# Inject storage client and close session at the end
def with_storage(func):
    def close_session(*args, **kwargs):
        with storage_client() as storage:
            res = func(*args, storage=storage, **kwargs)
        return res
    return close_session


# Inject user
def jwt_required(func):
    def get_user(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            raise UnAuthorized('JWT Authentication failed: {}'.format(e))
        jwt_user = get_jwt_identity()
        user = kwargs['storage'].users.get(email=jwt_user)
        res = func(*args, user=user, **kwargs)
        return res
    return get_user


# authorize only admins
def admin_only(func):
    def has_permissions(*args, **kwargs):
        if kwargs['user'].role != 'Administrator':
            raise UnAuthorized('User with role {} is not authorized')
        return func(*args, **kwargs)
    return has_permissions


# authorize editor role and above
def editor_only(func):
    def has_permissions(*args, **kwargs):
        if kwargs['user'].role not in ['Administrator', 'Editor']:
            raise UnAuthorized('User with role {} is not authorized')
        return func(*args, **kwargs)
    return has_permissions
