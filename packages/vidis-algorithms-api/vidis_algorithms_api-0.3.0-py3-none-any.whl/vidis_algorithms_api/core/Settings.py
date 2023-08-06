import os

from pydantic import AmqpDsn, BaseSettings, RedisDsn


class Settings(BaseSettings):
    DATA_PATH: str
    CELERY_BROKER: AmqpDsn
    CELERY_BACKEND: RedisDsn

    CUSTOM_LAYER_FOLDER = 'custom_algorithm'
