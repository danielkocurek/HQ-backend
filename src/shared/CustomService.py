
from flask import Response, json


def custom_response(res, status_code):
    """Custom Response Function

    Args:
        res (json): response data
        status_code (int): status code
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status = status_code
    )