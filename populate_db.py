import csv
import models 
from datetime import datetime

def create_table(engine):
    models.meta.create_all(engine)

def populate_file(fileName,engine):
    with engine.connect() as connection:
        with connection.begin():
            with open(fileName,'r',newline='') as csvfile:
                lines = csvfile.readlines()[2:]
                spamreader = csv.reader(lines, delimiter=',', quotechar='|')
                for row in spamreader:
                    connection.execute(models.price.insert(), {"currency": row[2], "date": datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'),"price":float(row[6])})

def populate_db(engine):
    create_table(engine)
    populate_file('Kucoin_BTCUSDT_d.csv',engine)
    populate_file('Kucoin_ETHUSDT_d.csv',engine)
    populate_file('Kucoin_LTCUSDT_d.csv',engine)
