from runtime import Args
from typing import TypedDict
import requests
from bs4 import BeautifulSoup

# Define the input type for the plugin
class Input(TypedDict):
    url: str

# Define the output type for the plugin
class Output(TypedDict):
    title: str
    date: str
    author: str
    description: str
    image: str
    url: str

def handler(args: Args[Input]) -> Output:
    """
    Parses the given URL to extract structured information such as the page title,
    publication date, author, meta description, and an image link.

    Parameters
    ----------
    args : Args[Input]
        An object containing the input parameters, specifically:
        - url (str): The URL of the web page to parse.

    Returns
    -------
    Output
        A dictionary containing the extracted information:
        - title (str): The title of the web page.
        - date (str): The publication date of the content (if available).
        - author (str): The author of the content (if available).
        - description (str): The meta description of the page.
        - image (str): The primary image link (if available).
        - url (str): The original URL passed as input.
    """
    # Extract the URL from input
    url = args.input.get('url')

    # Validate the URL
    if not url:
        raise ValueError("No URL provided.")

    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch the URL: {e}")

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract structured data
    title = soup.title.string if soup.title else "No title found"
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else "No description found"
    author_tag = soup.find('meta', attrs={'name': 'author'})
    author = author_tag['content'] if author_tag else "No author found"
    date_tag = soup.find('meta', attrs={'property': 'article:published_time'})
    date = date_tag['content'] if date_tag else "No date found"
    image_tag = soup.find('meta', attrs={'property': 'og:image'})
    image = image_tag['content'] if image_tag else "No image link found"

    # Return the structured output
    return {
        "title": title,
        "date": date,
        "author": author,
        "description": description,
        "image": image,
        "url": url
    }
