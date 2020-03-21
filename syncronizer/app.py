import sys
sys.path.append('../')
import os 
from scheduler import Scheduler
from flask import Flask
from healthz_controller import healthz_controller
from shared.log import Log

_http_port=int(os.getenv('CASE_HTTP_PORT', 8001))
_logging = Log('werkzeug').logger()

if __name__ == "__main__":
    Scheduler()
    app = Flask(__name__)
    app.register_blueprint(healthz_controller, url_prefix='/healthz')
    app.run('0.0.0.0', port=_http_port)


