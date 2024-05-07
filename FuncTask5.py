import requests

def search_movie_images(title, api_key, cx):
    # Define the Google Custom Search API endpoint
    endpoint = "https://www.googleapis.com/customsearch/v1"

    # Construct the search query
    params = {
        "q": title + " movie",
        "cx": cx,  # Your custom search engine ID
        "key": api_key,  # Your API key
        "searchType": "image",
        "num": 5  # Number of images to retrieve
    }

    # Send GET request to the Google Custom Search API
    response = requests.get(endpoint, params=params)
    data = response.json()

    # Parse the response and extract image URLs
    image_urls = [item["link"] for item in data.get("items", [])]

    return image_urls

# Example usage
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"  # Replace with your API key
    cx = "YOUR_CX"  # Replace with your Custom Search Engine ID
    title = input("Enter a movie title: ")
    image_urls = search_movie_images(title, api_key, cx)
    print(image_urls)
