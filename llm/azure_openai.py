import os
import re

from openai import AzureOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

load_dotenv()


def get_openai_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )


def get_structured_completion(
    prompt: str,
    response_model: type[BaseModel],
    model: str | None = None
) -> BaseModel:
    model = model or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
    client = get_openai_client()

    messages = [
        {"role": "system", "content": "You are an expert financial analyst."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_model
        )
        return response.choices[0].message.parsed

    except openai.BadRequestError as exc:
        msg = str(exc)
        if "response_format" in msg or "json_schema" in msg or "Structured Outputs" in msg:
            fallback = client.chat.completions.create(model=model, messages=messages)
            text = fallback.choices[0].message.content
            match = re.search(r"\{.*\}", text, re.S)
            json_text = match.group(0) if match else text
            if hasattr(response_model, "model_validate_json"):
                return response_model.model_validate_json(json_text)
            return response_model.parse_raw(json_text)
        raise
