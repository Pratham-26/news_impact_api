# News Impact Analysis API

A FastAPI-based service that analyzes news articles and provides impact analysis using LLM models.

## Features

- Extract article content from URLs
- Analyze news article impact using LLM models (supports DeepSeek and other models)
- RESTful API with automatic documentation
- Docker support for easy deployment
- Comprehensive logging system

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (if running locally)
- API keys for LLM services (if using OpenAI)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Configure environment variables:
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_key_here
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at http://localhost:5000

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn get_news_impact:app --reload --host 0.0.0.0 --port 5000
```

## API Documentation

### Endpoints

#### POST /api/news-impact

Analyzes a news article and returns its impact analysis.

**Request Body:**
```json
{
    "url": "https://example.com/news-article",
    "model": "deepseek/deepseek-r1:free"  // optional, defaults to deepseek
}
```

**Response:**
```json
{
    "article": {
        "title": "Article Title",
        "content": "Article Content",
        "url": "Article URL"
    },
    "impact_analysis": {
        // LLM-generated analysis
    }
}
```

### Interactive Documentation

- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

## Project Structure

```
.
├── get_news_impact.py     # Main FastAPI application
├── utils/
│   └── html_extractor.py  # Article extraction utilities
├── llm_calls/
│   └── llm.py            # LLM integration
├── logs/                  # Log files directory
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── requirements.txt      # Python dependencies
```

## Configuration

### Environment Variables

- `ENVIRONMENT`: Set to 'production' or 'development'
- `OPENAI_API_KEY`: OpenAI API key (if using OpenAI models)

### Logging

Logs are stored in `logs/news_impact.log` and include:
- Article extraction attempts
- LLM analysis requests
- Error messages and stack traces

## Error Handling

The API includes comprehensive error handling for:
- Invalid URLs
- Failed article extraction
- LLM service errors
- Rate limiting
- Network issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here] 