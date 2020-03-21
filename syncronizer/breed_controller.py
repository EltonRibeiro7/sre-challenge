import sys
sys.path.append('../')
import os, timeit
from shared.request import Request
from shared.log import Log
from shared.model import Breed, BreedImage, BreedTemperament, Temperament, Origin

class BreedController():
    _base_api_address = 'https://api.thecatapi.com'
    _request_key = {'x-api-key': os.getenv('CASE_REQUEST_KEY', 'afc36b2f-de9c-4db0-afe2-a4c54ee843e0')}
    _request_timeout = float(os.getenv('CASE_REQUEST_TIMEOUT', 30))

    def syncronize_breeds(self):
        _start_time = timeit.default_timer()
        try:
            self._logging.info('Getting breed information on endpoint {} with an defined timeout of {} seconds(s)'.format(self._base_api_address, self._request_timeout))
            _breeds = self._request.get(self._base_api_address+'/v1/breeds', timeout=self._request_timeout,  headers=self._request_key).json()
            self._logging.debug(_breeds)

        except Exception  as err:
            self._logging.error('Error while trying to get breed info, details: {}'.format(err))
            raise

        else:
            for _breed_item in _breeds:
                try:
                    self._logging.info('Updating data on database {}'.format(_breed_item['name']))
                    self._logging.debug(_breed_item)
                    
                    _origin, _origin_created = Origin.get_or_create(
                                                            name = _breed_item['origin']
                                                            )
                    self._logging.info('Created origin record {}'.format(_origin.name) if _origin_created else 'Origin record alreay exists{}'.format(_origin.name))


                    _breed, _breed_created = Breed.get_or_create(
                                                    id=_breed_item['id'],
                                                    name=_breed_item['name'],
                                                    origin_id=_origin.id,
                                                    description=_breed_item['description'],
                                                    )
                    self._logging.info('Created breed record {}'.format(_breed.name) if _breed_created else 'Breed record alreay exists{}'.format(_breed.name))


                    for _temperament in set(_breed_item['temperament'].split(',')):
                        self._logging.debug(_temperament)
                        _temperament, _temperament_created = Temperament.get_or_create(
                                                                            name = str(_temperament).strip()
                                                                            )
                        self._logging.info('Created temperament record {}'.format(_temperament.name) if _temperament_created else 'Temperament record alreay exists {}'.format(_breed.name))

                        _breed_temperament, _breed_temperament_created = BreedTemperament.get_or_create(
                                                                                    breed_id = _breed.id, 
                                                                                    temperament_id = _temperament.id
                                                                                    )
                    
                        self._logging.info('Created breed_temperament record {}'.format(_breed_temperament.id) if _breed_temperament_created else 'BreedTemperament record alreay exists {}'.format(_breed_temperament.id))

                except Exception as err:
                    self._logging.error('Error while trying to save on database, details {}'.format(err))
                    raise
                
        self._logging.info('Sync completed, total exec time: {:.3f} seconds'.format((timeit.default_timer() - _start_time)))
        

    def syncronize_breed_images(self):
        _start_time = timeit.default_timer()
        try:
            self._logging.info('Retrieving records from database')
            _records = Breed.select(Breed.id)
            self._logging.debug(_records)
        except Exception as err:
            self._logging.error('Error while trying to retrieve records, details {}'.format(err))
            raise

        else:
            for _record_item in _records:
                _query_params = {
                    'breed_id': _record_item,
                    'limit': '3',
                    'size': 'med',
                    'order': 'ASC'
                }
                try:
                    self._logging.info('Getting images urls by breed_id')
                    self._logging.debug(_record_item)
                    _images = self._request.get(self._base_api_address+'/v1/images/search', timeout=self._request_timeout,  headers=self._request_key, params=_query_params).json()

                except Exception as err:
                    self._logging.error('Error while getting image urls, details {}'.format(err))
                    raise

                else:
                    for _image_item in _images:
                        self._logging.debug(_image_item)
                        try:
                            self._logging.info('Updating data on database {}'.format(_image_item['id']))
                            self._logging.debug(_image_item)
                            _image, _image_created = BreedImage.get_or_create(
                                                    id=_image_item['id'],
                                                    breed_id=_record_item,
                                                    url=_image_item['url'])
                            self._logging.info('Breed image created record for image id {}'.format(_image_item['id']) if _image_created else 'Breed image already exists for image id {}'.format(_image_item['id']))

                        except Exception as err:
                            self._logging.error('Error while trying to save on database, details {}'.format(err))
                            raise

        self._logging.info('Sync completed, total exec time: {:.3f} seconds'.format((timeit.default_timer() - _start_time)))
                      
    def __init__(self):
        self._logging = Log('breed_controller').logger()
        self._request = Request().request_with_retry()

if __name__ == "__main__":
    BreedController()