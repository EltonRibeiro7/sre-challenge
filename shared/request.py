import sys
sys.path.append('../')
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectTimeout, ConnectionError, HTTPError
from urllib3.util.retry import Retry
from shared.log import Log
import requests

class Request():

    def request_with_retry(self, retries=3, session=None, backoff_factor=0.3):
        self._session = session
        self._session = requests.Session()
        self._retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            method_whitelist=False,
        )

        self._adapter = HTTPAdapter(max_retries=self._retry)
        self._session.mount('http://', self._adapter)
        self._session.mount('https://', self._adapter)
        
        return self._session
    
    def __init__(self):
        self._logging = Log('request').logger()

if __name__ == "__main__":
    pass