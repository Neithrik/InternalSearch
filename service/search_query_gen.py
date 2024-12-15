

from typing import List
from pydantic import BaseModel

from openai_client import make_openai_request


PROMPT = """
We are building an application that searches through Notion pages and Slack messages to find answers to questions. To get the most relevant results, we need to generate search queries of varying specificity.

For the following question, generate a list of search queries from most specific to most general:
 - The question itself (e.g., "What is the capital of the France?")
 - The search query with at most 4 words (e.g., "Capital of the France")
 - The search query with at most 3 words (e.g., "The France Capital") 
 - The search query with at most 2 words (e.g., "Capital France")
 - The search query with at most 1 word (e.g., "France")

This will help us search both Notion and Slack effectively by trying different variations of the query.

Question: {question}
"""


class SearchQueries(BaseModel):
    queries: List[str]

async def generate_search_queries(question: str) -> SearchQueries:
    prompt = PROMPT.format(question=question)
    response = await make_openai_request(
        model="gpt-4o",
        prompt=prompt,
        response_format=SearchQueries
    )
    return response
