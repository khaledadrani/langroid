from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    APP_HOST: str = Field(env="APP_HOST", default="localhost")
    APP_PORT: int = Field(env="APP_PORT", default=8000)
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="Langroid")
    ROOT_PATH: str = Field(env="ROOT_PATH", default="/api")
    API_VERSION: str = Field(env="API_VERSION", default='/v1')

    DEBUG: bool = Field(description="Use this to enable dev and debugging features", default=False)


class DataBaseConfig(BaseSettings):
    """Configuration class for connecting to the accompanying cahpp_database"""
    DB_HOST: str = Field(env='DB_HOST', default='localhost',
                         description="Host for running the cahpp_database instance")
    DB_PORT: int = Field(env='DB_PORT', default=5433, description="Port for running the cahpp_database instance")
    DB_NAME: str = Field(env='DB_NAME', default='domtik_database', description="Database name")
    DB_USER: str = Field(env='DB_USER', default='postgres', description="Username to access the cahpp_database")
    DB_PASSWORD: str = Field(env='DB_PASSWORD', default='root', description="Account password")

    @property
    def db_url(self):
        return f"postgresql://{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}" \
               f"?user={self.DB_USER}&password={self.DB_PASSWORD}"

    @property
    def async_url(self) -> str:  # TODO should review test this
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@lru_cache(maxsize=1)  # TODO test this
def get_settings():
    return AppConfig()
