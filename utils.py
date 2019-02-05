from flask import make_response, jsonify, current_app
import json

def resp_success(message, data={}, status_code=200):
    responseObject = {
        'status_code': status_code,
        'message': message,
        'data': data
    }
    return make_response(jsonify(responseObject)), status_code


def resp_fail(message, data={}, status_code=400):
    responseObject = {
        'status_code': status_code,
        'message': message,
        'data': data
    }
    return make_response(jsonify(responseObject)), status_code