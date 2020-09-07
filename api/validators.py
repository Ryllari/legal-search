import re
from flask import request
from functools import wraps

from .constants import AVAILABLE_TR
from .http_utils import bad_request_error


def validate_process_number(process_number: str):
    # Verify process_number format (CNJ standard) with J equals to 8
    if not re.fullmatch(r'^\d{7}-\d{2}.\d{4}.8.\d{2}.\d{4}$', process_number):
        raise bad_request_error("Invalid process number format. Use CNJ standard for legal process numbering "
                                "(NNNNNNN-DD.AAAA.J.TR.OOOO) with 'J' value equals to 8")

    # Verify process_number with TR available for search
    tr = process_number.split('.')[3]
    if tr not in AVAILABLE_TR:
        raise bad_request_error(f'Search unavailable for this TR. Availables TRs: {list(AVAILABLE_TR.keys())}')


def validate_request_data(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Verify if is a valid json
        data = request.json or {}
        if not data:
            raise bad_request_error('Request body must be a valid json')

        # Verify missing field
        if not data.get('process_number', ''):
            raise bad_request_error('Missing process number to search')

        # Verify if is a valid input data (process_number)
        validate_process_number(data['process_number'])

        return f(*args, **kwargs)
    return wrapper
