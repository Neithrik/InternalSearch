export interface SearchResponse {
    response: string,
    sources: string[]
}

export const searchApi = async (question: string): Promise<SearchResponse> => {
    const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
    });

    if (!response.ok) {
        throw new Error('Search request failed');
    }

    return response.json();
};
