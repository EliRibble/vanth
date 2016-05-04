import sepiida.endpoints
import sepiida.fields

import vanth.platform.user


class User(sepiida.endpoints.APIEndpoint):
    ENDPOINT = '/user/'
    SIGNATURE = sepiida.fields.JSONObject(s={
        'name'      : sepiida.fields.String(),
        'password'  : sepiida.fields.String(),
        'username'  : sepiida.fields.String(),
    })

    @staticmethod
    def post(payload):
        uri = vanth.platform.user.create(payload['name'], payload['username'], payload['password'])

        return None, 204, {'Location': uri}

    @staticmethod
    def get(uuid): # pylint: disable=unused-argument
        return {}
