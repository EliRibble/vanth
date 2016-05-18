import sepiida.endpoints
import sepiida.fields

import vanth.platform.ofxsource


class OFXSource(sepiida.endpoints.APIEndpoint):
    ENDPOINT = '/ofxsource/'
    SIGNATURE = sepiida.fields.JSONObject(s={
        'name'      : sepiida.fields.String(),
        'fid'       : sepiida.fields.String(),
        'bankid'    : sepiida.fields.String(),
        'uri'       : sepiida.fields.URI('ofxsource'),
    })
    @staticmethod
    def list():
        return vanth.platform.ofxsource.by_filter({})


    @staticmethod
    def get(uuid):
        return vanth.platform.ofxsource.by_filter({'uuid': [str(uuid)]})[0]
