import os
from typing import List
from slack_sdk import WebClient
import asyncio

from models import Document, DocumentSource
from config import SLACK_TOKEN

async def make_slack_search_request(queries: List[str]) -> list[Document]:
    client = WebClient(token=SLACK_TOKEN)
    
    # Try queries from most specific to most general until we find results
    for query in queries:
        print(f"Trying query: {query}")
        # Use asyncio.to_thread to run the synchronous slack API call in a separate thread
        response = await asyncio.to_thread(client.search_messages, query=query)
        print(response)

        if response["ok"]:
            messages = response["messages"]["matches"]
            if messages:  # If we found any matches
                # Convert Slack messages to Document objects
                documents = [
                    Document(
                        source=DocumentSource.SLACK,
                        content=msg["text"],
                        link=msg["permalink"]  # Slack message permalink
                    )
                    for msg in messages
                ]
                return documents
    
    # If no results found with any query
    return []
