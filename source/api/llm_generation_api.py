from typing import Dict

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from starlette.requests import Request

from source.configuration.constants import gpt4all_mistral_template
from source.configuration.injection import DependencyContainer
from source.schema.api_schema import SimpleLLMRequest
from source.services.simple_llm_service import LLMService

llm_generation_api = APIRouter(prefix='/llm', tags=["LLM generation"])


@llm_generation_api.post(
    "",
    response_model=Dict
)
@inject
async def generate_llm_sync(request_data: SimpleLLMRequest,
                            llm_service: LLMService = Depends(
                                Provide[DependencyContainer.llm_service]),
                            ):
    return await llm_service.generate_answer(prompt=request_data.prompt,
                                             model_type=request_data.llm_type,
                                             model_params=request_data.params.model_dump()
                                             )


@llm_generation_api.post(
    "/stream",
    response_model=Dict
)
@inject
async def stream_llm(request_data: SimpleLLMRequest,
                     request: Request,
                     llm_service: LLMService = Depends(
                         Provide[DependencyContainer.llm_service]),
                     ):
    return StreamingResponse(llm_service.stream_response(prompt=request_data.prompt,
                                                         model_type=request_data.llm_type,
                                                         request=request
                                                         ), media_type="text/event-stream")


@llm_generation_api.post(
    "/prompt/template",
    response_model=Dict
)
def return_gpt4all_template():
    return {"template": gpt4all_mistral_template}
