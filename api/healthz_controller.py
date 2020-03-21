import sys
sys.path.append('../')
from flask import Blueprint, jsonify, make_response
from shared.log import Log

healthz_controller = Blueprint('healthz_ontroller', __name__)
_logging = Log('healthz_controller').logger()

@healthz_controller.route('/', methods=['GET'])
def healthz():
    _response = make_response(jsonify({'status': 'working'}), 200)
    return _response

if __name__ == "__main__":
    pass