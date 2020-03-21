import sys
sys.path.append('../')
import os 
from shared.log import Log
from swagger_ui import flask_api_doc
from flask import Flask, make_response, jsonify
from healthz_controller import  healthz_controller
from breed_controller import  breed_controller
from prometheus_flask_exporter import PrometheusMetrics
import json

_http_port=int(os.getenv('CASE_HTTP_PORT', 8000))
_logging = Log('werkzeug').logger()

app = Flask(__name__)
metrics = PrometheusMetrics(app)
flask_api_doc(app, config_path='./docs/swagger.json', url_prefix='/api/swagger', title='ITAU SRE CASE')


@app.errorhandler(404)
@metrics.do_not_track()
def error_not_found(e):
    _logging.info('Not found')
    return make_response(jsonify({'message': 'not found'}), 404)

@app.errorhandler(500)
def error_exception(e):
    _logging.error('Error while processing request')
    return make_response(jsonify({'message': 'error while processing request'}), 500)

if __name__ == "__main__":
    app.register_blueprint(breed_controller, url_prefix='/api/v1/breeds')
    app.register_blueprint(healthz_controller, url_prefix='/healthz')
    app.run('0.0.0.0', port=_http_port)