import logging, os
class Log():

    _FORMAT="%(asctime)s ; %(levelname)s ; %(name)s ; %(funcName)s ; %(process)d ; message: %(message)s"
    _formatter= logging.Formatter(_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    _logging_level=os.getenv('CASE_LOGGING_LEVEL', 'INFO')

    
    def __init__ (self, _logger:str='root'):
        self._logger = logging.getLogger(_logger)
        self._logger.setLevel(self._logging_level)
        _handler = logging.StreamHandler()
        _handler.setLevel(self._logging_level)
        _handler.setFormatter(self._formatter)
        self._logger.addHandler(_handler)

    def logger(self):
        return self._logger
        
if __name__ == "__main__":
    pass

