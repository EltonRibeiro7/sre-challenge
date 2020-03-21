import sys
sys.path.append('../')
import sys, os, timeit
from shared.request import Request
from shared.log import Log
from shared.model import  Category, CategoryImage

class CategoryController():
    _base_api_address = 'https://api.thecatapi.com'
    _request_key = {'x-api-key': os.getenv('CASE_REQUEST_KEY', 'afc36b2f-de9c-4db0-afe2-a4c54ee843e0')}
    _request_timeout = float(os.getenv('CASE_REQUEST_TIMEOUT', 30))
    _categories_name = ['hats', 'sunglasses'] 

    def syncronize_category(self):
        _start_time = timeit.default_timer()
        try:
            self._logging.info('Getting category information on endpoint {} with an defined timeout of {} seconds(s)'.format(self._base_api_address, self._request_timeout))
            _categories = self._request.get(self._base_api_address+'/v1/categories', timeout=self._request_timeout, headers=self._request_key).json()            
            self._logging.debug(_categories)

        except Exception  as err:
            self._logging.error('Error while trying to get category info, details: {}'.format(err))
            raise
        
        else:
            for _category_item in _categories:
                try:
                    self._logging.info('Updating data on database {}'.format(_category_item['name']))
                    self._logging.debug(_category_item)
                    _category, _category_created = Category.get_or_create(
                                            category_id=_category_item['id'],
                                            name=_category_item['name']
                                            )
                    self._logging.info('Category created record {}'.format(_category.name) if _category_created else 'Category record already exists {}'.format(_category.name))

                except Exception as err:
                    self._logging.error('Error while trying to save on database {}'.format(err))
                    raise

        self._logging.info('Category sync completed, total exec time: {:.3f} seconds '.format(timeit.default_timer() - _start_time))

    def syncronize_category_images(self):
        _start_time = timeit.default_timer()
        try:
            self._logging.info('Retrieving records from database')
            _records = Category.select(Category.category_id).where(Category.name.in_(self._categories_name))
            self._logging.debug(_records)

        except Exception as err:
            self._logging.error('Error while trying to retrieve records, details {}'.format(err))
            raise

        else:
            for _record_item in _records:
                _query_params = {
                    'category_ids': _record_item,
                    'limit': '3',
                    'size': 'med',
                    'order': 'ASC'
                }
                try:
                    self._logging.info('Getting images urls by category_id')
                    self._logging.debug(_query_params)
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
                            _image, _image_created = CategoryImage.get_or_create(
                                                    id=_image_item['id'],
                                                    category_id=_record_item,
                                                    url=_image_item['url']
                                                    )
                            self._logging.info('Category image created record for image id {}'.format(_image_item['id']) if _image_created else 'Category image record already exists for image id {}'.format(_image_item['id']))

                        except Exception as err:
                            self._logging.error('Error while trying to save on database, details {}'.format(err))
                            raise

        self._logging.info('Sync completed, total exec time: {:.3f} seconds'.format((timeit.default_timer() - _start_time)))

    def __init__(self):
        self._logging = Log('category_controller').logger()
        self._request = Request().request_with_retry()

if __name__ == "__main__":
    CategoryController()