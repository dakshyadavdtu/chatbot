import random
import logging

# Default fallback responses when the ML model cannot generate a good response
FALLBACK_RESPONSES = [
    "I'm not sure I understand. Could you rephrase that?",
    "I don't have an answer for that right now. Could you ask something else?",
    "I'm still learning! That's a bit beyond my current knowledge.",
    "Interesting question! I don't have a specific answer for that yet.",
    "I'm not sure about that. Is there something else I can help with?",
    "I'm having trouble understanding that request. Could you try again?",
    "I don't have enough information to answer that question properly.",
    "That's a good question, but I don't have a good answer for it yet.",
    "I'm sorry, I couldn't process that correctly. Could you try asking differently?"
]

# Greeting responses
GREETING_RESPONSES = [
    "Hello! How can I help you today?",
    "Hi there! What can I do for you?",
    "Greetings! How may I assist you?",
    "Hey! What can I help you with today?",
    "Hello! I'm here to help. What do you need?"
]

# Farewell responses
FAREWELL_RESPONSES = [
    "Goodbye! Have a great day!",
    "See you later! Feel free to chat again anytime.",
    "Bye for now! Come back if you have more questions.",
    "Farewell! Thanks for chatting.",
    "Take care! I'll be here if you need help again."
]

# Thankful responses
THANKFUL_RESPONSES = [
    "You're welcome!",
    "Happy to help!",
    "No problem at all!",
    "Anytime! That's what I'm here for.",
    "Glad I could be of assistance!"
]

def get_fallback_response():
    """
    Get a random fallback response
    
    Returns:
        str: A fallback response
    """
    return random.choice(FALLBACK_RESPONSES)

def get_greeting_response():
    """
    Get a random greeting response
    
    Returns:
        str: A greeting response
    """
    return random.choice(GREETING_RESPONSES)

def get_farewell_response():
    """
    Get a random farewell response
    
    Returns:
        str: A farewell response
    """
    return random.choice(FAREWELL_RESPONSES)

def get_thankful_response():
    """
    Get a random thankful response
    
    Returns:
        str: A thankful response
    """
    return random.choice(THANKFUL_RESPONSES)

def is_greeting(text):
    """
    Check if the text is a greeting
    
    Args:
        text (str): The input text
        
    Returns:
        bool: True if the text is a greeting, False otherwise
    """
    greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    return any(greeting in text.lower() for greeting in greetings)

def is_farewell(text):
    """
    Check if the text is a farewell
    
    Args:
        text (str): The input text
        
    Returns:
        bool: True if the text is a farewell, False otherwise
    """
    farewells = ['bye', 'goodbye', 'see you', 'talk later', 'have a good day']
    return any(farewell in text.lower() for farewell in farewells)

def is_thankful(text):
    """
    Check if the text expresses gratitude
    
    Args:
        text (str): The input text
        
    Returns:
        bool: True if the text expresses gratitude, False otherwise
    """
    gratitude = ['thank you', 'thanks', 'appreciate it', 'grateful']
    return any(phrase in text.lower() for phrase in gratitude)

def get_response_based_on_type(text):
    """
    Get a response based on the type of input
    
    Args:
        text (str): The input text
        
    Returns:
        str: A response based on the type of input
    """
    try:
        # Check the type of input
        if is_greeting(text):
            return get_greeting_response()
        elif is_farewell(text):
            return get_farewell_response()
        elif is_thankful(text):
            return get_thankful_response()
        else:
            # Return None to indicate no specific response type was detected
            return None
    except Exception as e:
        logging.error(f"Error getting response based on type: {e}")
        return None
