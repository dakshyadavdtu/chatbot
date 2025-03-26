import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import logging

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    # Downloads with verbose output so we can see any issues
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

# Make sure all needed resources are downloaded
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)  # Download punkt_tab specifically since it's needed
nltk.download('stopwords', quiet=True)  
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)  # Open Multilingual WordNet

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Get stopwords
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    Preprocess the text by performing the following steps:
    1. Convert to lowercase
    2. Remove punctuation
    3. Remove numbers
    4. Tokenize the text
    5. Remove stopwords
    6. Lemmatize the words
    
    Args:
        text (str): The input text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not text:
        return ""
        
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Simple tokenization fallback in case NLTK tokenizer fails
        try:
            tokens = word_tokenize(text)
        except Exception as token_error:
            logging.error(f"Tokenization error: {token_error}. Using simple split fallback.")
            tokens = text.split()
        
        # Remove stopwords and lemmatize with safeguards
        filtered_tokens = []
        for word in tokens:
            if word and word not in stop_words:
                try:
                    lemmatized = lemmatizer.lemmatize(word)
                    filtered_tokens.append(lemmatized)
                except Exception as lemma_error:
                    logging.error(f"Lemmatization error for word '{word}': {lemma_error}")
                    filtered_tokens.append(word)  # Use original word if lemmatization fails
        
        # Join the tokens back into a string
        preprocessed_text = ' '.join(filtered_tokens)
        
        # If somehow we get an empty string, return the original
        if not preprocessed_text:
            return text
            
        return preprocessed_text
    except Exception as e:
        logging.error(f"Error preprocessing text: {e}")
        return text  # Return original text if preprocessing fails

def extract_entities(text):
    """
    Extract entities from the text that might be useful for the chatbot
    
    Args:
        text (str): The input text
        
    Returns:
        dict: Extracted entities
    """
    entities = {}
    
    # Extract greeting patterns
    greeting_patterns = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    if any(greeting in text.lower() for greeting in greeting_patterns):
        entities['is_greeting'] = True
    
    # Extract question patterns
    question_patterns = ['what', 'who', 'where', 'when', 'why', 'how', '?']
    if any(question in text.lower() for question in question_patterns):
        entities['is_question'] = True
    
    # Extract farewell patterns
    farewell_patterns = ['bye', 'goodbye', 'see you', 'talk later', 'have a good day']
    if any(farewell in text.lower() for farewell in farewell_patterns):
        entities['is_farewell'] = True
    
    return entities
