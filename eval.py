# eval.py
import asyncio
from generate_end_response import generate_response
from result_scorer import is_document_relevant
from search_query_gen import generate_search_queries
from slack import make_slack_search_request
from notion import make_notion_search_request
import click

@click.command()
@click.argument('question')
def main(question: str):
    """Search Notion with the provided query."""
    
    async def async_search() -> str:
        queries = await generate_search_queries(question)
        print(queries)
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

        print(relevant_results)
        response = await generate_response(relevant_results, question)
        print(response)

    return asyncio.run(async_search())

if __name__ == "__main__":
    main()
