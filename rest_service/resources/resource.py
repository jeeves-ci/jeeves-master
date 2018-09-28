from flask_restful import Resource


class JeevesResource(Resource):

    # This was helpful: https://stackoverflow.com/questions/32500073/
    # request-header-field-access-control-allow-headers-is-not-
    # allowed-by-itself-in-pr
    def options(self, **kwargs):
        return None, 200, {'Access-Control-Allow-Origin': '*',
                           'Allow': 'GET,HEAD,OPTIONS,POST,PUT',
                           "Access-Control-Allow-Headers": "Content-Type,"
                                                           "Authorization"}
