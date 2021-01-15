import os

import yaml


class Config:
    profile = ''
    jwt_secret = ''
    data_host = ''
    tpv_user = ''
    tpv_core = ''


def __init_config():
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yml')
    config_data = yaml.safe_load(open(file))
    Config.profile = config_data['profile']
    print("Configuring App... ", Config.profile)
    Config.jwt_secret = __read_environments(config_data[Config.profile]['jwt_secret'])
    Config.data_host = __read_environments(config_data[Config.profile]['data_host'])
    Config.tpv_user = __read_environments(config_data[Config.profile]['tpv_user'])
    Config.tpv_core = __read_environments(config_data[Config.profile]['tpv_core'])


def __read_environments(key) -> str:
    start = key.find('${')
    while start != -1:
        end = key.find('}')
        env = key[start + 2:end]
        key = key.replace('${' + env + '}', os.getenv(env, '?'))
        start = key.find('${')
    return key


__init_config()
