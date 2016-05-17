import json

import flask
import sepiida.endpoints
import sepiida.fields

import vanth.auth
import vanth.errors
import vanth.platform.user
import vanth.user


class Session(sepiida.endpoints.APIEndpoint):
    ENDPOINT = '/session/'
    SIGNATURE = sepiida.fields.JSONObject(s={
        'username'  : sepiida.fields.String(),
        'password'  : sepiida.fields.String(methods=['POST']),
    })
    @staticmethod
    def post(payload):
        user = vanth.platform.user.by_credentials(payload['username'], payload['password'])
        if not user:
            raise vanth.errors.InvalidCredentials()
        vanth.auth.set_session(user)

    @staticmethod
    def get(uuid): # pylint: disable=unused-argument
        user = vanth.auth.current_user()
        del user['password']
        if not user:
            raise vanth.errors.ResourceDoesNotExist("You are not currently authenticated and therefore do not have a session")
        return user

    def list(self):
        payload = self.get(None)
        return flask.make_response(json.dumps(payload), 200, {'Content-Type': 'application/json'})
