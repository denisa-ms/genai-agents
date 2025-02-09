from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_GPT4_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

class LLMProviderSettings(BaseSettings):
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3


class AzureOpenAISettings(LLMProviderSettings):
    base_url: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key: str = os.getenv("AZURE_OPENAI_API_KEY")
    api_version: str = os.getenv("AZURE_OPENAI_API_VERSION")
    default_model: str = os.getenv("AZURE_OPENAI_GPT4o_DEPLOYMENT_NAME")


class LlamaSettings(LLMProviderSettings):
    base_url: str = "http://localhost:11434/v1"
    api_key: str = "key"  # required, but not used
    api_version: str = "version"  # required, but not used
    default_model: str = "llama3"
    

class Settings(BaseSettings):
    app_name: str = "GenAI Project Template"
    openai: AzureOpenAISettings = AzureOpenAISettings()
    llama: LlamaSettings = LlamaSettings()


def get_settings():
    return Settings()