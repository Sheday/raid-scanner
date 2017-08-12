from config import *
from peewee import *
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import requests, pdb

db = MySQLDatabase(DB_NAME, host = HOST, port = PORT, user = USER, passwd = PASSWORD)

class Base(Model):
    class Meta:
        database = db

class Raid(Base):
    level = IntegerField()
    pokemon = CharField()
    starts_at = DateTimeField()
    expires_at = DateTimeField()
    location = CharField()
    location_name = CharField()

    class Meta:
        indexes = (
            (('starts_at', 'location_name'), True),
        )

if __name__ == "__main__":
    print "Creating database table..."
    try:
        Raid.create_table()
        print "Database table created. Run main.py to get data."
    except OperationalError:
        print "Database table already exists. Run main.py to get data."
