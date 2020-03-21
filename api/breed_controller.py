import sys
sys.path.append('../')
from flask import Blueprint, jsonify, make_response, request
from shared.model import Breed, Origin, Temperament, BreedTemperament, db_close, db_connect
from shared.log import Log
from playhouse.shortcuts import model_to_dict

_logging = Log('breed_controller').logger()

breed_controller = Blueprint('breed_controller', __name__)


@breed_controller.route('/', methods=['GET'])
def breeds():
    _args = request.args
    _logging.debug(_args.items())
    if not _args:
        return get_all_breeds()

    elif 'temperament' in _args:
        return get_breed_by_temperament(_args['temperament'])

    elif 'origin' in _args:
        return get_breed_by_origin(_args['origin'])

    elif 'err' in _args:
        return err_request(_args['err'])

    else:
        return bad_request()

@breed_controller.route('/<string:breed_id>', methods=['GET'])
def breed_by_id(breed_id):
    return get_breed_by_id(breed_id)

def get_all_breeds():
    try:
        _logging.info('Getting All Breeds')
        _breeds = Breed.select(Breed.name, Breed.id)
        if len(_breeds) == 0:
            return not_found()

        else:
            _breeds_list = []
            for _breed in _breeds:
                _breeds_list.append(model_to_dict(_breed, only=[Breed.id, Breed.name]))
            _response =  make_response(jsonify(_breeds_list), 200)
            _logging.debug(_response)
            return _response

    except Exception as err:
        _logging.error('Error while querying database, details: {} '.format(err))
        
        raise

def get_breed_by_id(_breed_id:str):
    try:
        _logging.info('Getting breed info by id')
        _breed = Breed.get_or_none(Breed.id == _breed_id)
        _logging.debug(_breed)
        if _breed is None:
            _logging.info('Breed id not found')
            
            return not_found()

        else:
            _temperaments = []
            _breed_dict = model_to_dict(_breed, backrefs=True)
            for _temperament in _breed_dict['temperaments']:
                _temperaments.append(_temperament['temperament_id']['name'])

            _breed_dict['temperaments'] = str(_temperaments).strip('[]').replace("'", "")
            _breed_dict['temperament'] = _breed_dict.pop('temperaments')
            _breed_dict['origin'] = _breed_dict.pop('origin_id')
            _breed_dict['origin'] = _breed_dict['origin']['name']
            _response =  make_response(jsonify(_breed_dict), 200)
            _logging.debug(_response)
            return _response

    except Exception as err:
        _logging.error('Error while querying database, details: {} '.format(err))
        
        raise

def get_breed_by_temperament(_temperament:str):
    try:
        _logging.info('Getting breed by temperament')
        _breeds = Breed.select(Breed.id, Breed.name).join(BreedTemperament).join(Temperament).where(Temperament.name == _temperament)
        _logging.debug(_breeds)
        if len(_breeds) == 0:
            _logging.info('Temperament not found')
            return not_found()

        else:
            _breeds_list = []
            for _breed in _breeds:
                _breeds_list.append(model_to_dict(_breed, only=[Breed.id, Breed.name]))
            _response =  make_response(jsonify(_breeds_list), 200)
            _logging.debug(_response)
            return _response

    except Exception as err:
        _logging.error('Error while querying database, details: {} '.format(err))
        raise

def get_breed_by_origin(_origin:str):
    try:
        _logging.info('Getting breed by origin')
        _breeds = Breed.select().join(Origin).where(Origin.name == _origin)
        _logging.debug(_breeds)
        if len(_breeds) == 0:
            
            _logging.info('Origin not found')
            return not_found()

        else:
            _breeds_list = []
            for _breed in _breeds:
                _breeds_list.append(model_to_dict(_breed, only=[Breed.id, Breed.name]))
            _response =  make_response(jsonify(_breeds_list), 200)
            _logging.debug(_response)            
            return _response

    except Exception as err:
        _logging.error('Error while querying database, details: {} '.format(err))
        raise

def not_found():
    _logging.info('Not found')
    return make_response(jsonify({'message': 'not found'}), 404)


def bad_request():
    _logging.warning('Bad Request')
    return make_response(jsonify({'message': 'bad request'}), 400)

def err_request(_err):
    _logging.error('Error Request')
    return make_response(jsonify({'message': 'error request: {}'.format(_err)}), 500)

@breed_controller.before_request
def _db_connect():
    db_connect()


@breed_controller.teardown_request
def _db_close(ext):
    db_close()