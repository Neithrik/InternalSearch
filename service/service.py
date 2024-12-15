# eval.py
from flask import Flask, request, jsonify
import asyncio
from generate_end_response import generate_response
from result_scorer import is_document_relevant
from search_query_gen import generate_search_queries
from slack import make_slack_search_request
from notion import make_notion_search_request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

async def async_search(question: str) -> str:
    queries = await generate_search_queries(question)
    # Run searches in parallel
    slack_task = asyncio.create_task(make_slack_search_request(queries.queries))
    notion_task = asyncio.create_task(make_notion_search_request(queries.queries))
    
    # Wait for both searches to complete
    slack_results, notion_results = await asyncio.gather(slack_task, notion_task)

    # Combine results
    all_results = notion_results + slack_results
    
    # Filter results by relevance
    # Create tasks for checking relevance in parallel
    relevance_tasks = [is_document_relevant(result, question) for result in all_results]
    # Wait for all relevance checks to complete
    relevance_results = await asyncio.gather(*relevance_tasks)
    
    # Filter results based on relevance checks
    relevant_results = [
        result for result, is_relevant in zip(all_results, relevance_results) 
        if is_relevant
    ]

    response = await generate_response(relevant_results, question)
    return response.model_dump_json()

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400
    
    question = data['question']
    result = asyncio.run(async_search(question))
    return result

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
