import requests

def search_movie_soundtrack(title, api_key, cx):
    # Define the Google Custom Search API endpoint
    endpoint = "https://www.googleapis.com/customsearch/v1"

    # Construct the search query to focus on finding the movie soundtrack
    params = {
        "q": title + " soundtrack",
        "cx": cx,  # Your custom search engine ID
        "key": api_key,  # Your API key
        "num": 5  # Number of search results to retrieve
    }

    # Send GET request to the Google Custom Search API
    response = requests.get(endpoint, params=params)
    data = response.json()

    # Parse the response and extract relevant webpages URLs
    webpage_urls = [item["link"] for item in data.get("items", [])]

    return webpage_urls

# Example usage
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"  # Replace with your API key
    cx = "YOUR_CX"  # Replace with your Custom Search Engine ID
    title = input("Enter a movie title: ")
    webpage_urls = search_movie_soundtrack(title, api_key, cx)
    print(webpage_urls)
