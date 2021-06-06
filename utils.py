
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request():
    return error_response(400, 'Bad request')


def not_found():
    return error_response(404, 'Resource not found')


def internal_error():
    return error_response(500, 'Internal error')
