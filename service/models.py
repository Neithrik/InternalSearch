from enum import Enum
from typing import List
from pydantic import BaseModel

class DocumentSource(Enum):
    SLACK = "slack"
    NOTION = "notion"

class Document(BaseModel):
    source: DocumentSource
    content: str
    link: str

class GeneratedResponse(BaseModel):
    response: str
    sources: List[str]
