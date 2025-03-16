import requests
from bs4 import BeautifulSoup
import os
import logging

# Configure logging for the HTML extractor
html_extractor_log_path = 'logs/html_extractor.log'

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(html_extractor_log_path),
        logging.StreamHandler()
    ]
)
html_extractor_logger = logging.getLogger('html_extractor')


def extract_article_data(url: str) -> dict:
    """Extracts title, summary, and content from a news article at the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'No title found'

        # Extract summary (assuming it's in a <meta> tag with name="description")
        summary = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'No summary found'

        # Extract content (assuming it's in <article> tag)
        content = soup.find('article').get_text(strip=True) if soup.find('article') else 'No content found'

        logging.info(f"Article data extracted successfully from {url}")
        return {
            'title': title,
            'summary': summary,
            'content': content
        }
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the URL {url}: {e}")
        return {}

