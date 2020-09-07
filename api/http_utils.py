from werkzeug.exceptions import HTTPException


# Create a Bad Request error
def bad_request_error(description):
    error = HTTPException(description=description)
    error.code = 400
    return error


# Create a Not Found error
def not_found_error(description):
    error = HTTPException(description=description)
    error.code = 404
    return error
