from mongoengine import connect

from src.config import Config
from src.data.seeder_dev import delete_all_and_seed_database


def start_database():
    connect('tpv2', host=Config.data_host)  # host: localhost, port: 27017, password:'', authentication_source=''
    if Config.profile in ["dev", "prod"]:
        delete_all_and_seed_database()
