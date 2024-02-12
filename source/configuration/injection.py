from dependency_injector import containers, providers

from source.configuration.config import AppConfig
from source.services.simple_llm_service import LLMService


class DependencyContainer(containers.DeclarativeContainer):
    """Container class for dependency injection"""
    wiring_config = containers.WiringConfiguration(packages=["source"])
    app_config = providers.Singleton(AppConfig)

    llm_service = providers.Singleton(LLMService)
