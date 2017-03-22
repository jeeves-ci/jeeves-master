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
