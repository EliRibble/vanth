import sepiida.endpoints
import sepiida.errors
import sepiida.fields

import vanth.platform.user


class User(sepiida.endpoints.APIEndpoint):
    ENDPOINT = '/user/'
    SIGNATURE = sepiida.fields.JSONObject(s={
        'name'      : sepiida.fields.String(),
        'password'  : sepiida.fields.String(methods=['POST', 'PUT']),
        'username'  : sepiida.fields.String(),
    })

    @staticmethod
    def post(payload):
        uri = vanth.platform.user.create(payload['name'], payload['username'], payload['password'])
        vanth.auth.set_session({
            'name'      : payload['name'],
            'uri'       : uri,
            'username'  : payload['username'],
        })

        return None, 204, {'Location': uri}

    @staticmethod
    def get(uuid):
        users = vanth.platform.user.by_filter({'uuid': [str(uuid)]})
        if not users:
            raise sepiida.errors.ResourceNotFound()
        return users[0]
