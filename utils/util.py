import json

from flask import request


def get_value(string):
    return request.form.get(string)


def decode_response_to_json(response):
    return json.loads(response.data.decode('utf-8').replace("'", "\""))
