import os

from gpt4all import GPT4All
from loguru import logger
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from source.configuration.config import LLMConfig
from source.exceptions.core_exceptions import UnknownModelType
from source.domain.implementations.fake_llm import FakeListLLM
from source.schema.common_schema import SupportedLLModels


class LLMFactory:
    def __init__(self, config: LLMConfig):
        self.config = config

    def __call__(self, model_type: SupportedLLModels):
        config = self.config
        match model_type:  # match requires probably python 3.10 or more
            case SupportedLLModels.gpt4all:
                return GPT4All(model_name=self.config.MODEL_NAME,
                               model_path=self.config.MODEL_PATH,
                               verbose=False)
            case SupportedLLModels.gpt2:
                tokenizer = AutoTokenizer.from_pretrained("gpt2")
                model = AutoModelForCausalLM.from_pretrained(config.model_path)
                return pipeline(
                    "text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200
                )

            case SupportedLLModels.fake:
                with open("static/mock_llm_response.txt", 'r') as f:
                    responses = [
                        str(f.read()),
                    ]
                    return FakeListLLM(responses=responses)

            case _default:
                logger.error(f"Model {model_type} not supported!")
                raise UnknownModelType(detail=f"Unknown Model Type: {model_type}")

    @staticmethod
    def download_model(model_url, model_path):
        logger.info("Downloading Model Files ... Please wait")
        if os.path.exists(model_path):
            logger.info("Model already exists .. Skipping download!")
        else:
            response = requests.get(model_url)
            response.raise_for_status()

            with open(model_path, 'wb') as model_file:
                model_file.write(response.content)
            logger.success("Model Files Downloaded!")
