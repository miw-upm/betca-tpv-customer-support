import logging

from mongoengine import connect, disconnect

from src.config import Config
from src.data.seeder_dev import delete_all_and_seed_database


def start_database():
    logging.info("Connecting database tpv2... " + Config.data_host)
    disconnect()
    connect('tpv2', host=Config.data_host)  # host: localhost, port: 27017, password:'', authentication_source=''
    if Config.profile in ["debug", "dev", "prod"]:  # "prod" only because it is staging
        delete_all_and_seed_database()

