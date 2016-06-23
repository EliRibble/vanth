import functools
import json

import flask


def parse(args):
    def _decorate(request_handler):
        @functools.wraps(request_handler)
        def _parse():
            values = {}
            missing_parameters = []
            for key, converter in args.items():
                supplied = flask.request.form.get(key)
                if supplied is None:
                    missing_parameters.append(key)
                else:
                    values[key] = converter(supplied)
            if missing_parameters:
                return (json.dumps({'errors': [{
                    'title' : "Missing required paramter '{}'".format(parameter),
                    'code'  : "missing-required-paramter",
                } for parameter in missing_parameters]}), 400, {})
            return request_handler(values)
        return _parse
    return _decorate
