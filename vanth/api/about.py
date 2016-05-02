import json

import flask
import sepiida.endpoints
import sepiida.fields

from vanth.version import VERSION


class About(sepiida.endpoints.APIEndpoint):
    ENDPOINT = "/about/"
    SIGNATURE = sepiida.fields.JSONObject(s={
        'version'   : sepiida.fields.String()
    })
    PUBLIC_METHODS = ['list']
    @staticmethod
    def list():
        return flask.make_response(json.dumps({'version': VERSION}), 200)
