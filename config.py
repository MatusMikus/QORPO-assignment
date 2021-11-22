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
    path_to_db = pathlib.Path(dbConfig['db_name'])
    db_exists = path_to_db.is_file()
    
    engine = create_engine('sqlite+pysqlite:///{}'.format("test"))
    
    if not db_exists:
        # engine = create_engine('mysql+mysqldb://{0}:{1}@{2}'.format(dbConfig['username'], dbConfig['password'], dbConfig['host']))
        # existing_databases = engine.execute("SHOW DATABASES;")
        # existing_databases = [d[0] for d in existing_databases]

        # if dbConfig['db_name'] not in existing_databases:
        #     engine.execute("CREATE DATABASE {0}".format(dbConfig['db_name']))    
        #     #db_engine = create_engine(
        #         # 'mysql+mysqldb://{0}:{1}@{2}/{3}'.format(dbConfig['username'], dbConfig['password'], dbConfig['host'], dbConfig['db_name']),
        #         #pool_size=20)
        populate_db.create_table(engine)
        populate_db.populate_file('Kucoin_BTCUSDT_d.csv',engine)
        populate_db.populate_file('Kucoin_ETHUSDT_d.csv',engine)
        populate_db.populate_file('Kucoin_LTCUSDT_d.csv',engine)
        # else:
        #     db_engine = create_engine(
        #         'mysql+mysqldb://{0}:{1}@{2}/{3}'.format(dbConfig['username'], dbConfig['password'], dbConfig['host'], dbConfig['db_name']),
        #         pool_size=20
        #     )

    app['db'] = engine
    app['db_connect'] = engine.connect()

    yield

    app['db_connect'].close()
    app['db'].dispose()
    
