# eval.py
from flask import Flask, request, jsonify
import asyncio
from generate_end_response import generate_response
from result_scorer import is_document_relevant
from search_query_gen import generate_search_queries
from slack import make_slack_search_request
from notion import make_notion_search_request
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app)

async def async_search(question: str) -> str:
    queries = await generate_search_queries(question)
    slack_results = make_slack_search_request(queries.queries)
    notion_results = make_notion_search_request(queries.queries)

    # Combine results
    all_results = notion_results + slack_results
    
    # Filter results by relevance
    relevant_results = []
    for result in all_results:
        is_relevant = await is_document_relevant(result, question)
        if is_relevant:
            relevant_results.append(result)

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
