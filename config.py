from sqlalchemy import create_engine
from populate_db import populate_db
import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent
config_path = BASE_DIR / 'config.yaml'

def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config

config = get_config(config_path)
dbConfig = config['db']

async def context(app):
    path_to_db = pathlib.Path(dbConfig['db_name'])
    db_exists = path_to_db.is_file()
    
    engine = create_engine('sqlite+pysqlite:///{}'.format(dbConfig['db_name']))
    app['db'] = engine
    app['db_connect'] = engine.connect()

    if not db_exists:
        populate_db(app['db'],app['db_connect']) #reuse connection

    yield

    app['db_connect'].close()
    app['db'].dispose()
    
