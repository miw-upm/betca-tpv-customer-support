from typing import Optional

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    ENVIRONMENT: str = Field(None, env="ENVIRONMENT")
    JWT_SECRET: Optional[str]
    DATA_HOST: Optional[str]
    TPV: Optional[str]
    TPV_USER: Optional[str]
    TPV_CORE: Optional[str]

    class Config:
        env_file: str = "config.env"


class DevConfig(Config):
    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(Config):
    class Config:
        env_prefix: str = "PROD_"


def get_config():
    if "prod" == Config().ENVIRONMENT:
        return ProdConfig()
    else:
        return DevConfig()


config = get_config()
