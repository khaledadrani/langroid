# import logging
# import os
# import time
# from pathlib import PurePath
# from typing import Type, AsyncGenerator
#
# import torch
# from fastapi.requests import Request
# from pydantic import ValidationError
#
# from source.configuration.config import LLMConfig
# from source.domain.interfaces.base_llm import BaseLLM
#
# if False:
#     from transformers import AutoTokenizer, pipeline
#     from attention_sinks import AutoModelForCausalLM
# else:
#     from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
#
#
# class HuggingFaceLLM(BaseLLM):
#     def __init__(self,
#                  config: LLMConfig,
#                  model_class: Type[AutoModelForCausalLM] = AutoModelForCausalLM,
#                  tokenizer_class: Type[AutoTokenizer] = AutoTokenizer):
#         super().__init__()
#         self.config = config
#         # self.model_directory = os.path.join(model_directory, model_name.split("/")[-1])
#         self.tokenizer = AutoTokenizer.from_pretrained(self.config.MODEL_NAME)
#         self.model = None
#         self.inference_pipeline = None
#
#         # Defining decoding parameters
#         self.decoding_parameters = dict()
#         if self.config.MODEL_TASK.upper() == Tasks.CHAT:
#             self.decoding_parameters["repetition_penalty"] = self.config.REPETITION_PENALTY
#             self.decoding_parameters["no_repeat_ngram_size"] = self.config.NO_REPEAT_NGRAM_SIZE
#             self.decoding_parameters["use_cache"] = True
#
#         elif self.config.MODEL_TASK.upper() == Tasks.CODE_GENERATOR:
#             self.decoding_parameters["temperature"] = self.config.TEMPERATURE
#             self.decoding_parameters["top_k"] = self.config.TOP_K
#             self.decoding_parameters["top_p"] = self.config.TOP_P
#         else:
#             raise ModelLoadError(detail=f"Unknown text generation task given: {self.config.MODEL_TASK}"
#                                         f"Please select one of the following tasks for this model:"
#                                         f"{[task for task in Tasks]}")
#
#         # we need to keep space for new tokens to be generated! TEHE!
#         self.allowed_prompt_length = self.tokenizer.model_max_length - self.config.MAX_NEW_TOKENS
#
#         self.model_name_string = PurePath(app_config.MODEL_NAME).name
#
#     def _create_instantiation_params(self) -> dict:
#         """
#         This method creates a dict containing the required params for model instantiation depending
#         on the environment variables and task.
#         :return: instantiation_params (dict)
#         """
#         instantiation_params = {
#             "pretrained_model_name_or_path": self.model_name,
#             "cache_dir": self.model_directory,
#             "trust_remote_code": False,
#             "device_map": self.config.DEVICE_MAP,
#             "load_in_8bit": self.config.EIGHT_BIT_LLM_QUANTIZATION,
#             "load_in_4bit": self.config.FOUR_BIT_LLM_QUANTIZATION
#         }
#
#         if self.config.USE_ATTENTION_SINK:
#             instantiation_params["attention_sink_size"] = self.config.ATTENTION_SINK_SIZE
#             instantiation_params["attention_sink_window_size"] = self.config.ATTENTION_SINK_WINDOW_SIZE
#             if self.config.MODEL_TASK != Tasks.CHAT:
#                 logger.warning(f"The use of attention sink is not intended to be used for the {self.config.MODEL_TASK}"
#                                f"Please set the model task to CHAT or disable attention sink.")
#
#         if self.config.FOUR_BIT_LLM_QUANTIZATION:
#             instantiation_params["bnb_4bit_compute_dtype"] = torch.float16
#             instantiation_params["bnb_4bit_quant_type"] = "nf4"
#             instantiation_params["bnb_4bit_use_double_quant"] = True
#
#         return instantiation_params
#
#     def load(self) -> AutoModelForCausalLM:
#         """
#         Wrapper for the HuggingFace model loading and downloading function.
#         :return: the loaded model.
#         """
#         return self.model_class.from_pretrained(**self._create_instantiation_params())
#
#     def create_pipeline(self) -> pipeline:
#         """
#         Creates a HuggingFace pipeline for text generation using the selected model.
#         :return: the created pipeline
#         """
#         pipeline_parameters = {"task": "text-generation",
#                                "model": self.model,
#                                "tokenizer": self.tokenizer,
#                                "torch_dtype": torch.int8,
#                                "trust_remote_code": True,
#                                "eos_token_id": self.tokenizer.eos_token_id,
#                                "device_map": self.config.DEVICE_MAP,
#                                }
#         try:
#             inference_pipeline = pipeline(**pipeline_parameters, **self.decoding_parameters)
#         except TypeError as model_loading_error:
#             raise ModelLoadError(
#                 detail=f"Unable to load the offline model {self.model_name}: {model_loading_error}"
#             )
#
#         logger.info("Pipeline created.")
#         return inference_pipeline
#
#     def predict(self, prompt: str, **kwargs) -> str:
#         """
#         Generates a response for the given prompt.
#         :param prompt: the input prompt
#         :return: model response
#         """
#         logger.warning("This function will be replaced by `generate_answer()` in a future version.")
#         prompt_length = len(self.tokenizer.encode(prompt))
#         if prompt_length > self.config.MAX_PROMPT_TOKEN_LENGTH:
#             raise PromptError(
#                 detail=f"The received prompt length ({prompt_length}) exceeds the "
#                        f"limit of {self.config.MAX_PROMPT_TOKEN_LENGTH}",
#             )
#
#         try:
#             results = self.inference_pipeline(
#                 prompt,
#                 return_full_text=False,
#                 max_new_tokens=self.config.MAX_NEW_TOKENS,
#             )
#
#         except RuntimeError as runtime_error:
#             raise ModelCallPredictionError(
#                 detail=f"Could not generate answer for prompt: {prompt}. Error: {runtime_error}")
#
#         except TypeError as model_loading_error:
#             raise ModelLoadError(
#                 detail=f"Offline model {self.model_name} not loaded: {model_loading_error}"
#             )
#         torch.cuda.empty_cache()
#         try:
#             return results[0].get("generated_text")
#         except (KeyError, ValueError) as parsing_error:
#             raise ResultParsingPredictionError(
#                 detail=f"Unable to parse model answer: {parsing_error}"
#             )
#
#     def get_metadata(self) -> dict:
#         """
#         Get the model hyperparameters and related configuration.
#         Returns:
#             dict: A dictionary containing the model metadata:
#         """
#         metadata = {"load_in_8bit": self.config.EIGHT_BIT_LLM_QUANTIZATION}
#         metadata["load_in_4bit"] = self.config.NO_REPEAT_NGRAM_SIZE
#         metadata["max_new_tokens"] = self.config.MAX_NEW_TOKENS
#         metadata["no_repeat_ngram_size"] = self.config.NO_REPEAT_NGRAM_SIZE
#         metadata["repetition_penalty"] = self.config.REPETITION_PENALTY
#         return metadata
#
#     def _validate_prompt(self, prompt: str, return_pt: bool = False) -> tuple[list[int], int]:
#         """
#         Validate prompt and returns the list of tokens if it is valid
#         :param prompt: str
#         :return: list of tokens (indexes), length of token list
#         """
#         tokens = self.tokenizer.encode(prompt, return_tensors="pt" if return_pt else None)
#         prompt_length = len(tokens)
#         if prompt_length > self.allowed_prompt_length:
#             message = (
#                 f"The received prompt length ({prompt_length}) exceeds the limit of "
#                 f"{self.allowed_prompt_length} tokens, with max new tokens set to "
#                 f"{self.config.MAX_NEW_TOKENS}, the model total capacity is {self.tokenizer.model_max_length}!"
#             )
#
#             logger.error(message)
#             raise PromptError(
#                 detail=message
#             )
#         return tokens, prompt_length
#
#     def generate_answer(self, prompt: str) -> ModelAnswer:
#         """
#         Generates an answer from the LLM given a prompt.
#         Args:
#             prompt: A text prompt upon which to generate an answer.
#
#         Returns:
#             ModelAnswer: the actual answer of the LLM and the inference time.
#         """
#
#         _, prompt_length = self._validate_prompt(prompt)
#
#         start_time = time.time()
#         try:
#             results = self.inference_pipeline(
#                 prompt,
#                 return_full_text=False,
#                 max_new_tokens=self.config.MAX_NEW_TOKENS,
#             )
#         except TypeError as model_loading_error:
#             raise ModelLoadError(
#                 detail=f"Offline model {self.model_name} not loaded: {model_loading_error}"
#             )
#
#         torch.cuda.empty_cache()
#         model_answer = {
#             "prompt_length": prompt_length,
#             "inference_time": time.time() - start_time,
#         }
#         try:
#             model_answer["model_name"] = self.model_name_string
#         except IndexError as index_error:
#             raise MetadataParsingError(
#                 detail=f"Unable to validate metadata format: {index_error}",
#             )
#         try:
#             model_answer["metadata"] = ModelMetadata(**self.get_metadata())
#         except ValidationError as validation_error:
#             raise MetadataParsingError(
#                 detail=f"Unable to validate metadata format: {validation_error}",
#             )
#         logger.info(
#             f"Prompt length: {model_answer['prompt_length']} |  "
#             f"Inference time: {model_answer['inference_time']} seconds."
#         )
#         try:
#             model_answer["response"] = results[0].get("generated_text")
#         except KeyError as key_error:
#             raise ResultParsingPredictionError(
#                 detail=f"Unable to parse response from model: {key_error}",
#             )
#         try:
#             return ModelAnswer(**model_answer)
#         except ValidationError as validation_error:
#             raise ResultParsingPredictionError(
#                 detail=f"Unable to validate model response format: {validation_error}",
#             )
#
#     def is_loaded_correctly(self) -> bool:
#         """
#         Checks if the  LLM is loaded as expected.
#         If local LLM loading is enabled, the model should not be None.
#         Returns: bool
#         """
#
#         return self.model is not None if app_config.LOAD_LOCAL_MODEL else True
#
#     async def aggregate_streaming_response(self, generated_tokens: list[str], prompt_length: int,
#                                            start_time: float) -> AsyncGenerator:
#         try:
#
#             yield str(ModelStreamingDoneResponse(
#                 detail="Success",
#                 data=ModelAnswer(
#                     response="".join(generated_tokens),
#                     metadata=ModelMetadata(**self.get_metadata()),
#                     model_name=self.model_name_string,
#                     prompt_length=prompt_length,
#                     inference_time=(time.time() - start_time)
#                 ))
#             )
#
#         except (IndexError, ValidationError) as error:
#             logger.error(error)
#             yield str(ModelStreamingErrorResponse(
#                 status=StreamingResponseStatus.ERROR,
#                 detail="Unable to parse response!")
#             )
#
#     async def generate_answer_by_streaming(self, prompt: str, request: Request) -> AsyncGenerator | None:
#         """
#         generate an answer from the model one token at a time
#         :param request:
#         :param prompt:
#         :return:
#         """
#         start_time = time.time()
#
#         input_ids, prompt_length = self._validate_prompt(prompt, return_pt=True)
#
#         generated_tokens = []
#         if await request.is_disconnected():
#             logger.warning("Connection disconnected!")
#             return
#         try:
#             # if an unexpected error occurs, break the streaming
#             for _ in range(self.config.MAX_NEW_TOKENS):
#
#                 if await request.is_disconnected():
#                     logger.warning("Connection disconnected, end streaming!")
#                     return
#                 # Generate one token at a time
#
#                 output = self.model.generate(input_ids,
#                                              max_length=input_ids.shape[1] + 1,
#                                              eos_token_id=self.tokenizer.eos_token_id,
#                                              **self.decoding_parameters)
#
#                 next_token = output[0, -1]  # Take the last token in the generated output
#                 next_token_str = self.tokenizer.decode(next_token, skip_special_tokens=True)
#
#                 if next_token == self.tokenizer.eos_token_id:
#                     logger.info(f"eos token detected, streaming completed with {len(generated_tokens)}")
#                     break
#
#                 generated_tokens.append(next_token_str)
#
#                 yield str(ModelStreamingInProgressResponse(
#                     data=next_token_str,
#                     detail="Streaming in progress!")
#                 )
#                 # Update input_ids with the newly generated token
#                 input_ids = output
#
#         except (TypeError, IndexError, RuntimeError) as error:
#             logger.error(f"Error while streaming: {error}")
#             yield str(ModelStreamingErrorResponse(
#                 detail="Error while streaming response!")
#             )
#             # if there is an error, break, do not continue yielding
#             return
#
#         torch.cuda.empty_cache()
#         logger.info(f"Max new tokens reached, streaming completed with {len(generated_tokens)}")
#
#         async for response in self.aggregate_streaming_response(generated_tokens=generated_tokens,
#                                                                 prompt_length=prompt_length,
#                                                                 start_time=start_time):
#             yield response
