from typing import List
from notion_client import Client
from config import NOTION_TOKEN
from models import Document, DocumentSource
import os

def extract_text_from_block(block):
    """Extract text content from different types of Notion blocks."""
    block_type = block['type']
    
    if block_type in ['paragraph', 'to_do', 'toggle']:
        # Get the rich_text array from the specific block type
        rich_text = block[block_type].get('rich_text', [])
        # Extract and join all plain_text content
        return ' '.join(text['plain_text'] for text in rich_text)
    
    return ''  # Return empty string for unsupported block types


def make_notion_search_request(queries: List[str]) -> list[Document]:
    notion = Client(auth=NOTION_TOKEN)
    
    # Try queries from most specific to most general until we find results
    for query in queries:
        print(f"Trying query: {query}")
        results = notion.search(query=query)
        
        if results['results']:  # If we found any matches
            documents = []
            for page in results['results']:
                # Get page title
                title = page['properties']['title']['title'][0]['plain_text']
                
                # Get page content
                page_id = page['id']
                page_content = notion.blocks.children.list(block_id=page_id)
                
                # Extract text from all blocks
                content_parts = []
                for block in page_content['results']:
                    text = extract_text_from_block(block)
                    if text:  # Only add non-empty content
                        content_parts.append(text)
                
                # Combine title and content with proper formatting
                full_content = f"{title}\n\n{'\n'.join(content_parts)}"
                
                doc = Document(
                    source=DocumentSource.NOTION,
                    content=full_content,
                    link=page['url']
                )
                documents.append(doc)
            
            return documents
    
    # If no results found with any query
    return []
