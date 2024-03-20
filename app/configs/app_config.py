from os.path import dirname, join

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = dirname(dirname(dirname(__file__)))
ENV_PATH = join(ROOT_DIR, '.env')


class AppConfig(BaseSettings):
    DBMS_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore')

    @property
    def db_url(self):
        return (
            f'{self.DBMS_NAME}+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


app_config = AppConfig()
