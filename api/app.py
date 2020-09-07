import json

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from api.constants import AVAILABLE_TR
from api.http_utils import not_found_error
from api.validators import validate_request_data

app = Flask(__name__)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """
    Handle any HTTPException to return response as json.
    """
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/')
def index():
    """
    Welcome endpoint. Return a json with project info.
    """
    return jsonify({
        "msg": "Welcome to the Legal Search API!",
        "links": {
            "api_doc": "https://documenter.getpostman.com/view/12464969/TVCiUmZZ",
            "github_repo": "https://github.com/Ryllari/legal-search"
        }
    })


@app.route('/search/', methods=['POST'])
@validate_request_data
def search():
    """
    Search process endpoint. Given a process number in the request body (process_number: str),
    it returns the process data.
    """
    process_number = request.json.get('process_number')

    # Find tribunal crawler by TR
    tr = process_number.split('.')[3]
    crawler_class = AVAILABLE_TR[tr]
    tribunal = crawler_class(process_number)

    info = tribunal.get_process_info()
    # Verifiy process data in tribunal
    if not (info.get('first_instance_data', {}) or info.get('second_instance_data', {})):
        raise not_found_error('No data found for this process number in any instance')

    return jsonify(info)
