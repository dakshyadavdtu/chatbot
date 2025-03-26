"""
Gemini API Client for enhanced chatbot responses
"""
import os
import logging
import google.generativeai as genai

# Configure logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure API key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

try:
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Try to list available models to help with debugging
    try:
        models = genai.list_models()
        model_names = [model.name for model in models]
        logger.info(f"Available Gemini models: {model_names}")
    except Exception as model_error:
        logger.error(f"Could not list models: {str(model_error)}")
    
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

def get_gemini_response(prompt, chat_history=None):
    """
    Get a response from the Gemini API
    
    Args:
        prompt (str): The user's input message
        chat_history (list, optional): Chat history for context
        
    Returns:
        str: Generated response from Gemini or None if error occurs
    """
    try:
        # Format the prompt with some context about the chatbot
        enhanced_prompt = f"You are a helpful assistant answering a user's question. Please provide a concise response to: {prompt}"
        
        # Initialize the model - use a model name that exists in the available models
        # Based on the list we retrieved, we should use models/gemini-1.5-pro or models/gemini-1.5-flash
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Generate content
        response = model.generate_content(enhanced_prompt)
        
        # Log and return the response
        logger.debug(f"Gemini response generated: {response.text}")
        return response.text
        
    except Exception as e:
        logger.error(f"Error getting Gemini response: {str(e)}")
        return None
