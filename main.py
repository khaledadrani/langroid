from fastapi import FastAPI

from source.api.llm_generation_api import llm_generation_api
from source.configuration.config import AppConfig
from source.configuration.injection import DependencyContainer

app_config = AppConfig()
app = FastAPI()
app.container = DependencyContainer()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


app.include_router(llm_generation_api, tags=["LLM GENERATION API"])

# Run the FastAPI application with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=app_config.APP_HOST, port=app_config.APP_PORT,
                workers=app_config.APP_WORKERS_COUNT)
