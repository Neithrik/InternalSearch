# At the top of your service.py
import os
from dotenv import load_dotenv
load_dotenv()  # This will load environment variables from .env file

# Create a .env file with:
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
SLACK_TOKEN=os.getenv('SLACK_TOKEN')
NOTION_TOKEN=os.getenv('NOTION_TOKEN')
