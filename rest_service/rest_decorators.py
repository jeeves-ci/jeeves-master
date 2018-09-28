from rest_service.storage import storage_client

from flask_restful import reqparse


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
            storage.close()
        return res
    return close_session
