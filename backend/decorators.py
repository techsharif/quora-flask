import json

from flask import Response, abort
from flask_restful import abort

from ResponseStatusException import ResponseStatusException


def response(status, message):
    return Response(
        message,
        mimetype="application/json",
        status=status
    )


def success(message):
    if message:
        return Response(
            json.dumps(message),
            mimetype="application/json",
            status=200)
    else:
        return Response(
            mimetype="application/json",
            status=200
        )


def response_filter(function):
    def wrapper(self):
        try:
            return success(function(self))
        except ResponseStatusException as rse:
            print(rse)
            res = response(
                rse.status,
                json.dumps({"message": rse.message}))

        except Exception as e:
            print(e)
            res = response(
                400,
                json.dumps({"message": "Unknown error"}))
        return abort(res)

    return wrapper
