import newspaper
import requests

def extract_text_from_url(url : str) -> str:
    """Extract author, date and text from the url

    Args:
        url (string): Link to the page
    """
    try:
        article = newspaper.article(url)
        text = f"Article authors : {article.authors}\nPublished date: {article.publish_date}\nArticle text : {article.text}"
        return text
    except Exception as e:
        print(e)
        raise Exception(f"Error in extracting text from url : {e}")