# run_local.py
import click
import requests

@click.command()
@click.argument('question')
def main(question: str):
    """Make a request to the local Flask service."""
    response = requests.post(
        'http://localhost:5000/search',
        json={"question": question}
    )
    result = response.json()
    print("\nQueries:", result.get("queries"))
    print("\nRelevant Results:", result.get("relevant_results"))
    print("\nResponse:", result.get("response"))

if __name__ == "__main__":
    main()
