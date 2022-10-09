import json

from flask import Response, abort, jsonify
from flask_restful import abort

from ResponseStatusException import ResponseStatusException


def response_filter(function):
    def wrapper(self):
        try:
            res = function(self)
            return jsonify(res) if res else {}
        except ResponseStatusException as rse:
            print(rse)
            res = Response(
                json.dumps({"message": rse.message}),
                mimetype="application/json",
                status=rse.status,
            )
        except Exception as e:
            print(e)
            res = Response(
                json.dumps({"message": "Unknown error"}),
                mimetype="application/json",
                status=400,
            )
        return abort(res)

    return wrapper
