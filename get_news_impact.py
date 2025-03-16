import os
import logging
from typing import Dict, Optional, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from utils.html_extractor import extract_article_data
from utils.html_extractor_news4k import extract_text_from_url
from llm_calls.llm import generate_response

# Configure logging
log_path = 'logs/news_impact.log'
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="News Impact Analysis API",
    description="An API that analyzes news articles and provides impact analysis using LLM models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class NewsImpactRequest(BaseModel):
    """
    Request model for news impact analysis.
    
    Attributes:
        url (HttpUrl): The URL of the news article to analyze
        model (str): The LLM model to use for analysis (defaults to deepseek)
    """
    url: HttpUrl
    model: str = "deepseek/deepseek-r1:free"
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com/news-article",
                "model": "deepseek/deepseek-r1:free"
            }
        }

def get_news_impact(url: str, model: str = "deepseek/deepseek-r1:free") -> Dict[str, Union[Dict, str]]:
    """
    Extracts article data from a URL and analyzes its impact using an LLM.
    
    Args:
        url (str): The URL of the news article to analyze
        model (str): The LLM model to use for analysis
        
    Returns:
        Dict[str, Union[Dict, str]]: A dictionary containing:
            - article: Dict containing article data (title, content, url)
            - impact_analysis: LLM-generated analysis
            - error: Error message if any
            
    Raises:
        Exception: If article extraction or LLM analysis fails
    """
    try:
        # Extract article data from the URL
        logger.info(f"Extracting article data from {url}")
        article_data = extract_text_from_url(url)
        logger.info(f"Article data extracted: {article_data}")
        
        if not article_data:
            logger.error(f"Failed to extract article data from {url}")
            return {"error": "Failed to extract article data"}
        
        # Generate impact analysis using LLM
        logger.info(f"Generating impact analysis using {model}")
        article_content = article_data
        impact_analysis = generate_response(article_content, "news", model)
        
        # Return combined results
        result = {
            "article": article_data,
            "impact_analysis": impact_analysis
        }
        
        logger.info(f"Successfully analyzed impact for article at {url}")
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing news impact: {str(e)}", exc_info=True)
        return {"error": str(e)}

@app.post("/api/news-impact", 
    response_model=Dict[str, Union[Dict, str]],
    summary="Analyze news article impact",
    description="Extracts content from a news article URL and analyzes its impact using LLM models")
async def news_impact_api(request: NewsImpactRequest) -> Dict[str, Union[Dict, str]]:
    """
    API endpoint to analyze the impact of a news article.
    
    Args:
        request (NewsImpactRequest): Request object containing URL and model choice
        
    Returns:
        Dict[str, Union[Dict, str]]: Analysis results or error message
        
    Raises:
        HTTPException: If the request fails or processing encounters an error
    """
    try:
        result = get_news_impact(str(request.url), request.model)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
        
    except Exception as e:
        logger.error(f"API error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)

