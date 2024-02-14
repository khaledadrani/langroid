import pathlib
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class CommonConfig(BaseSettings):
    ROOT_DIRECTORY: pathlib.Path = pathlib.Path(__file__).parent.parent.parent


class AppConfig(BaseSettings):
    APP_HOST: str = Field(default="localhost")
    APP_PORT: int = Field(default=8000)
    PROJECT_NAME: str = Field(default="Langroid")
    ROOT_PATH: str = Field(default="/api")
    API_VERSION: str = Field(default='/v1')
    APP_WORKERS_COUNT: int = Field(default=1)

    DEBUG: bool = Field(description="Use this to enable dev and debugging features", default=False)


class DataBaseConfig(BaseSettings):
    """Configuration class for connecting to the accompanying cahpp_database"""
    DB_HOST: str = Field(default='localhost',
                         description="Host for running the cahpp_database instance")
    DB_PORT: int = Field(default=5433, description="Port for running the cahpp_database instance")
    DB_NAME: str = Field(default='domtik_database', description="Database name")
    DB_USER: str = Field(default='postgres', description="Username to access the cahpp_database")
    DB_PASSWORD: str = Field(default='root', description="Account password")

    @property
    def db_url(self):
        return f"postgresql://{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}" \
               f"?user={self.DB_USER}&password={self.DB_PASSWORD}"


class LLMConfig(CommonConfig):
    MODEL_PATH: str = "./artifacts/"
    MODEL_NAME: str = 'gpt4all-falcon-newbpe-q4_0.gguf'


@lru_cache(maxsize=1)  # TODO test this
def get_settings():
    return AppConfig()
