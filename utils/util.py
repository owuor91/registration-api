from flask import request


def get_value(string):
    return request.form.get(string)
