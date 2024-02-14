import pathlib

ROOT_DIRECTORY: pathlib.Path = pathlib.Path(__file__).parent.parent.parent

gpt4all_mistral_template = '''
<|im_start|>system
{system_message}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
'''
gpt4all_mistral_prompt_example = '''
<|im_start|>system
You are a researcher in Harverd with great knowledge about all domains<|im_end|>
<|im_start|>user
Please provide a brief summary of the book "1984" by George Orwell.<|im_end|>
assistant
'''

gpt4all_falcon_template = "### Instruction: {user_prompt}\n### Response:"

# config management #static for now, no management from user? read only!
llm_list_config = {
    "GPT4ALL": {
        "FALCON": {  # initialization parameters
        },
        "MISTRAL": {},
        "ALL_MINI": {}
    },
    "FAKE": {
        "FAKE_LIST": {}
    }
}
