import sys
sys.path.append('../')
from peewee import * 
import os
from shared.log import Log
from playhouse.pool import PooledMySQLDatabase
from playhouse.migrate import MySQLMigrator


_db_host=os.getenv('CASE_DB_HOST', '127.0.0.1')
_db_port=int(os.getenv('CASE_DB_PORT', 3306))
_db_user=os.getenv('CASE_DB_USER', 'case_user')
_db_password=os.getenv('CASE_DB_PASSWORD', 'case_pass')
_db_name=os.getenv('CASE_DB_NAME', 'case_db')


_db = PooledMySQLDatabase(_db_name, max_connections=300, stale_timeout=5, host=_db_host, port=_db_port, user=_db_user, password=_db_password, )
_logging = Log('peewee').logger()

class BaseModel(Model):
    class Meta:
        database = _db

class Origin(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=100)
    class Meta:
        db_table = 'Origin'

class Breed(BaseModel):
    id = CharField(primary_key=True, max_length=50)
    origin_id = ForeignKeyField(Origin, index=True, backref='origin')
    name = CharField(max_length=200)
    description = CharField(max_length=1000, null=True)
    class Meta:
        db_table = 'Breed'

class Temperament(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=100, null=False)
    class Meta:
        db_table = 'Temperament'

class BreedTemperament(BaseModel):
    id = PrimaryKeyField()
    breed_id = ForeignKeyField(Breed, backref='temperaments', null=False)
    temperament_id = ForeignKeyField(Temperament, backref='temperaments', null=False)
    class Meta:
        db_table = 'Breed_Temperament'

class Category(BaseModel):
    category_id = BigIntegerField(primary_key=True)
    name = CharField(max_length=200, null=False)
    class Meta:
        db_table = 'Category'

class CategoryImage(BaseModel):
    id = CharField(primary_key=True, max_length=50)
    category_id = ForeignKeyField(Category, index=True, on_delete='CASCADE', backref='images')
    url = CharField(max_length=400)
    class Meta:
        db_table = 'CategoryImage'
    
class BreedImage(BaseModel):
    id = CharField(primary_key=True, max_length=50)
    breed_id = ForeignKeyField(Breed, index=True, on_delete='CASCADE', backref='images')
    url = CharField(max_length=400)
    class Meta:
        db_table = 'BreedImage'

def init_database():
    _CLASSES = [Breed, CategoryImage, BreedImage, Category, Origin, Temperament, BreedTemperament]
    try:
        _logging.info('Initializing database with name {}, on host {}, and port {}'.format(_db_name, _db_host, _db_port))
        _db.create_tables(_CLASSES)
        _logging.info('Database initialized')
    except Exception as err:
        _logging.error('Error while trying to initialize database, details {}'.format(err))
        raise

def db_connect():
    _logging.debug('Connecting to Database')
    _db.connect(reuse_if_open=True)

def db_close():
    if not _db.is_closed():
        _db.close()
        _logging.debug('Closing Connection to Database')


init_database()
