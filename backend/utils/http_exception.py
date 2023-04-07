from flask import make_response, abort

def http_exception(status_code: int, message: str | dict) -> None:
    response = make_response(message, status_code)
    abort(response)
