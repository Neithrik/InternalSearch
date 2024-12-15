import os

from typing import Type, TypeVar
from openai import AsyncOpenAI

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

API_KEY = os.getenv("OPENAI_API_KEY")

async def make_openai_request(model: str, prompt: str, response_format: Type[T]) -> T:
    client = AsyncOpenAI(api_key=API_KEY)
    response = await client.beta.chat.completions.parse(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format=response_format,
    )
    if response.choices[0].message.parsed is None:
        raise ValueError("OpenAI response parsing failed")
    return response.choices[0].message.parsed
