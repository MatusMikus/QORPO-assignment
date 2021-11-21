from sqlalchemy import create_engine
import populate_db
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
    engine = create_engine('mysql+mysqldb://{0}:{1}@{2}'.format(dbConfig['username'], dbConfig['password'], dbConfig['host']))

    existing_databases = engine.execute("SHOW DATABASES;")
    existing_databases = [d[0] for d in existing_databases]

    if dbConfig['db_name'] not in existing_databases:
        engine.execute("CREATE DATABASE {0}".format(dbConfig['db_name']))    
        db_engine = create_engine('mysql+mysqldb://{0}:{1}@{2}/{3}'.format(dbConfig['username'], dbConfig['password'], dbConfig['host'], dbConfig['db_name']))
        populate_db.create_table(engine)
        populate_db.populate_file('Kucoin_BTCUSDT_d.csv',engine)
        populate_db.populate_file('Kucoin_ETHUSDT_d.csv',engine)
        populate_db.populate_file('Kucoin_LTCUSDT_d.csv',engine)
    else:
        db_engine = create_engine('mysql+mysqldb://{0}:{1}@{2}/{3}'.format(dbConfig['username'], dbConfig['password'], dbConfig['host'], dbConfig['db_name']))

    app['db'] = db_engine

    yield

    app['db'].dispose()
