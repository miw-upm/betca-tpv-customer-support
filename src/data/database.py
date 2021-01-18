import logging

from mongoengine import connect, disconnect

from src.config import config
from src.data.seeder_dev import delete_all_and_seed_database


def start_database():
    logging.info("Connecting database tpv2... " + config.DATA_HOST)
    disconnect()
    connect('tpv2', host=config.DATA_HOST)  # host: localhost, port: 27017, password:'', authentication_source=''
    if config.ENVIRONMENT in ["dev", "prod"]:  # "prod" only because it is staging
        delete_all_and_seed_database()
