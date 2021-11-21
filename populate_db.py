import csv
import models 

def create_table(engine):
    models.meta.create_all(engine)

def populate_file(fileName,engine):
    with engine.connect() as connection:
        with connection.begin():
            with open(fileName,'r',newline='') as csvfile:
                lines = csvfile.readlines()[2:]
                spamreader = csv.reader(lines, delimiter=',', quotechar='|')
                for row in spamreader:
                    connection.execute(models.price.insert(), {"currency": row[2], "date": row[1],"price":float(row[6])})

