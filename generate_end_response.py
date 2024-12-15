from typing import List
from models import Document, GeneratedResponse
from openai_client import make_openai_request
from pydantic import BaseModel

class GeneratedResponseFormat(BaseModel):
    answer: str

PROMPT = """
You are a helpful assistant. Using the following documents as reference, please provide a concise, single-paragraph response to this question.
Your response should be no more than 3-4 sentences and include citations to the source documents using [1], [2], etc.

Question: {question}

Documents:
{numbered_documents}
"""

async def generate_response(documents: List[Document], question: str) -> GeneratedResponse:
    # Format documents with numbers for citation
    numbered_docs = []
    citations = []
    for i, doc in enumerate(documents, 1):
        numbered_docs.append(f"[{i}] Document from {doc.source.value} ({doc.link}):\n{doc.content}")
    
    docs_text = "\n\n".join(numbered_docs)
    
    # Generate response using OpenAI
    prompt = PROMPT.format(
        question=question, 
        numbered_documents=docs_text,
    )
    response = await make_openai_request(
        model="gpt-4o",
        prompt=prompt,
        response_format=GeneratedResponseFormat
    )

    # Return formatted response with sources
    return GeneratedResponse(
        response=response.answer,
        sources=[doc.link for doc in documents]
    )

