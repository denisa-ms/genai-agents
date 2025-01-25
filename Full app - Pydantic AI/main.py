from typing import Any, Dict, List, Type
import instructor
from openai import AzureOpenAI, OpenAI
from pydantic import BaseModel, Field

from infra.llm_factory import LLMFactory 
from  infra.settings import get_settings, AzureOpenAISettings, LlamaSettings, Settings, LLMProviderSettings

if __name__ == "__main__":

    class CompletionModel(BaseModel):
        response: str = Field(description="Your response to the user.")
        reasoning: str = Field(description="Explain your reasoning for the response.")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "If it takes 2 hours to dry 1 shirt out in the sun, how long will it take to dry 5 shirts?",
        },
    ]

    llm = LLMFactory("openai")
    completion = llm.create_completion(
        response_model=CompletionModel,
        messages=messages,
    )
    assert isinstance(completion, CompletionModel)

    print(f"Response: {completion.response}\n")
    print(f"Reasoning: {completion.reasoning}")