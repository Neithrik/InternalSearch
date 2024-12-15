from openai import BaseModel
from pydantic import ConfigDict
from models import Document
from openai_client import make_openai_request


PROMPT = """
You are a helpful assistant that evaluates the relevance of a document to a question.
Respond with JSON only:

{{
    "is_relevant": true
}}

Question: {question}

Document: {document}
"""

class RelevanceScore(BaseModel):
    model_config = ConfigDict(extra='forbid')  # Forbid additional properties
    is_relevant: bool


async def is_document_relevant(document: Document, question: str) -> bool:
    prompt = PROMPT.format(question=question, document=document.content)
    response = await make_openai_request(
        model="gpt-4o",
        prompt=prompt,
        response_format=RelevanceScore
    )
    return response.is_relevant
