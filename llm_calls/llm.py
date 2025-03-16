from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
import logging


#Create log directory if it doesn't exist
log_path = f'logs/llm_{datetime.now().strftime("%Y%m%d")}.log'

if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add file handler for detailed error logging
error_handler = logging.FileHandler(f'logs/llm_errors_{datetime.now().strftime("%Y%m%d")}.log')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s\nStack Trace: %(exc_info)s')
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)



client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= os.getenv("OPEN_ROUTER"),
)

def generate_prompt(text : str, prompt_type : str) -> str:
    """Method to generate prompt based on the prompt type
    """
    logger.info("Generating prompt")
    if prompt_type == "news":
        prompt_prefix = open("llm_calls/prompts/news_prompt.txt", "r", encoding="utf-8").read()
        prompt = f"{prompt_prefix}\n\n<article>Article text: {text}\n</article>"
        logger.info("Prompt generated")
        logger.info(prompt)
        return prompt


def generate_response(text : str,prompt_type : str, model : str = "deepseek/deepseek-r1:free") -> str:
    
    if model.startswith("deepseek"):
        completion = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": generate_prompt(text,prompt_type)
            }
        ]
        )
        
        
        logger.info("Response generated")
        logger.info(completion.choices[0].message.content)
        return completion.choices[0].message.content
