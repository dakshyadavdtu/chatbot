import os
import logging
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import psycopg2
from psycopg2 import Error
import mysql.connector
from mysql.connector import Error as MySQLError

# Determine database type
USE_MYSQL = os.environ.get('USE_MYSQL', 'false').lower() == 'true'

# Initialize the model pipeline
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)),
    ('clf', MultinomialNB())
])

# Check if a pre-trained model exists and load it
model_path = os.path.join(os.path.dirname(__file__), 'chatbot_model.pkl')
try:
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model_pipeline = pickle.load(f)
            logging.info("Loaded pre-trained model from disk")
except Exception as e:
    logging.error(f"Error loading pre-trained model: {e}")

# Flag to track if model needs training
model_trained = os.path.exists(model_path)

def get_training_data_from_db():
    """
    Fetch training data from the database (MySQL or PostgreSQL)
    
    Returns:
        tuple: (questions, answers) lists
    """
    questions = []
    answers = []
    
    if USE_MYSQL:
        # MySQL implementation
        try:
            # Get database connection details from environment variables
            db_config = {
                'host': os.environ.get('DB_HOST', 'localhost'),
                'database': os.environ.get('DB_NAME', 'chatbot'),
                'user': os.environ.get('DB_USER', 'root'),
                'password': os.environ.get('DB_PASSWORD', ''),
                'port': os.environ.get('DB_PORT', '3306')
            }
            
            # Connect to the MySQL database
            conn = mysql.connector.connect(**db_config)
            
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Query to get active training data
                query = "SELECT question, answer FROM training_data WHERE is_active = TRUE"
                cursor.execute(query)
                
                # Process the results
                for row in cursor.fetchall():
                    questions.append(row[0])  # First column is question
                    answers.append(row[1])    # Second column is answer
                
                cursor.close()
                conn.close()
                
                logging.info(f"Successfully retrieved {len(questions)} training data from MySQL")
        
        except MySQLError as e:
            logging.error(f"Error connecting to MySQL: {e}")
    
    else:
        # PostgreSQL implementation
        try:
            # Get database connection details from environment variables
            database_url = os.environ.get('DATABASE_URL')
            
            if not database_url:
                logging.error("DATABASE_URL not found in environment variables")
                return questions, answers
                
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(database_url)
            
            # Create a cursor
            cursor = conn.cursor()
            
            # Query to get active training data
            query = "SELECT question, answer FROM training_data WHERE is_active = TRUE"
            cursor.execute(query)
            
            # Process the results
            for row in cursor.fetchall():
                questions.append(row[0])  # First column is question
                answers.append(row[1])    # Second column is answer
            
            cursor.close()
            conn.close()
            
            logging.info(f"Successfully retrieved {len(questions)} training data from PostgreSQL")
        
        except Error as e:
            logging.error(f"Error connecting to PostgreSQL: {e}")
    
    return questions, answers

def load_default_training_data():
    """
    Load default training data if database fetch fails
    
    Returns:
        tuple: (questions, answers) lists
    """
    # Default training data with more varied responses
    questions = [
        # Greetings
        "hello",
        "hi",
        "hey there",
        "good morning",
        "good afternoon",
        "good evening",
        
        # General questions
        "how are you",
        "what is your name",
        "what can you do",
        "who made you",
        "what is your purpose",
        
        # Farewells
        "goodbye",
        "bye",
        "see you later",
        "talk to you later",
        
        # Gratitude
        "thank you",
        "thanks",
        "appreciate it",
        
        # Fun
        "tell me a joke",
        "say something funny",
        "another joke",
        
        # Knowledge
        "what is water",
        "what is ice",
        "what is the sun",
        "what is the moon",
        "what is a star",
        "who is the president",
        "what is a computer",
        "what is artificial intelligence",
        "what is machine learning",
        
        # Time-related (acknowledge limitations)
        "what time is it",
        "what day is it today",
        "what is the date",
        
        # Help
        "how does this work",
        "help me",
        "I need assistance",
        "how do I use this"
    ]
    
    answers = [
        # Greetings responses
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Hey! What can I help you with?",
        "Good morning! How can I assist you today?",
        "Good afternoon! How may I help you?",
        "Good evening! What can I do for you today?",
        
        # General question responses
        "I'm doing well, thank you for asking! How can I assist you?",
        "I'm a chatbot assistant. You can call me ChatBot.",
        "I can answer questions, have a conversation, and help you find information.",
        "I was created by a development team to assist users with information and conversation.",
        "I'm here to provide information, answer questions, and assist you with various tasks.",
        
        # Farewell responses
        "Goodbye! Feel free to chat again anytime.",
        "Bye! Have a great day!",
        "See you later! Come back if you need more help.",
        "Talk to you later! I'll be here when you need me.",
        
        # Gratitude responses
        "You're welcome! Is there anything else I can help with?",
        "Happy to help! Let me know if you need anything else.",
        "No problem at all! Feel free to ask if you have more questions.",
        
        # Fun responses
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a fake noodle? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        
        # Knowledge responses
        "Water is a transparent, tasteless, odorless, and nearly colorless chemical substance that is the main constituent of Earth's streams, lakes, and oceans, and the fluids of most living organisms.",
        "Ice is water frozen into a solid state. It can appear transparent or opaque bluish-white color depending on the presence of impurities or air inclusions.",
        "The Sun is the star at the center of our Solar System. It's a nearly perfect sphere of hot plasma, with internal convective motion that generates a magnetic field.",
        "The Moon is Earth's only natural satellite. It's about a quarter of Earth's diameter and is the fifth largest satellite in the Solar System.",
        "A star is an astronomical object consisting of a luminous spheroid of plasma held together by its own gravity.",
        "I don't have real-time information about current political leaders. You would need to check a reliable news source for up-to-date information.",
        "A computer is an electronic device that manipulates information, or data. It can store, retrieve, and process data.",
        "Artificial intelligence (AI) is intelligence demonstrated by machines, unlike the natural intelligence displayed by humans and animals.",
        "Machine learning is a field of inquiry devoted to understanding and building methods that 'learn', that is, methods that leverage data to improve performance on some set of tasks.",
        
        # Time-related responses (acknowledge limitations)
        "I don't have access to real-time information like the current time. You can check your device's clock for that information.",
        "I don't have access to real-time calendar information. You can check your device's calendar for the current date.",
        "I don't have access to the current date. You might want to check your device's calendar for that information.",
        
        # Help responses
        "You can type any message or question, and I'll try to respond appropriately. I can provide information on various topics or just chat.",
        "I'm here to assist you. Just type your question or what you need help with, and I'll do my best to help you.",
        "What do you need assistance with? Feel free to ask any question, and I'll try to provide a helpful response.",
        "This is a chat interface. Simply type your message or question, and I'll respond as helpfully as I can."
    ]
    
    return questions, answers

def train_model():
    """
    Train the ML model using data from the database or fallback to default data
    """
    global model_trained, model_pipeline
    
    # First try to get training data from database
    questions, answers = get_training_data_from_db()
    
    # If no data from database, use default training data
    if not questions:
        questions, answers = load_default_training_data()
    
    if questions:
        try:
            # Train the model
            model_pipeline.fit(questions, answers)
            
            # Save the trained model
            with open(model_path, 'wb') as f:
                pickle.dump(model_pipeline, f)
            
            model_trained = True
            logging.info("Model trained and saved successfully")
        except Exception as e:
            logging.error(f"Error training model: {e}")
    else:
        logging.error("No training data available")

def get_response(text):
    """
    Get a response from the ML model based on the input text
    
    Args:
        text (str): Preprocessed user input
        
    Returns:
        str: Bot response from the ML model or None if prediction fails
    """
    global model_trained
    
    # If model is not trained, train it first
    if not model_trained:
        train_model()
    
    try:
        # Get prediction from model
        if text and model_trained:
            # Convert input to proper format for prediction
            text_input = [text]
            
            try:
                # Make prediction
                prediction = model_pipeline.predict(text_input)
                
                # Return the predicted response
                if prediction and len(prediction) > 0:
                    return prediction[0]
                else:
                    logging.error("Prediction was empty")
            except Exception as prediction_error:
                logging.error(f"Error making prediction: {prediction_error}")
                
            # If prediction fails or is empty, use default data more intelligently
            questions, answers = load_default_training_data()
            
            # First try direct matching
            for i, question in enumerate(questions):
                if text.lower() in question.lower() or question.lower() in text.lower():
                    logging.info(f"Direct match found for query: {text}")
                    return answers[i]
            
            # If no direct match, try word-level matching
            text_words = set(text.lower().split())
            best_match = None
            best_score = 0
            
            for i, question in enumerate(questions):
                question_words = set(question.lower().split())
                common_words = text_words.intersection(question_words)
                
                # Calculate a simple overlap score
                if len(question_words) > 0:
                    score = len(common_words) / len(question_words)
                    
                    if score > best_score:
                        best_score = score
                        best_match = i
            
            # Use the best match if score is above threshold
            if best_match is not None and best_score > 0.3:
                logging.info(f"Word match found for query: {text} (score: {best_score})")
                return answers[best_match]
            
            # If all else fails, return a randomly selected response
            import random
            logging.info(f"Using random response for query: {text}")
            return random.choice([
                "I'm not sure I understand that. Could you rephrase?",
                "That's an interesting question. I'll need to learn more about that.",
                "I don't have specific information on that topic yet.",
                "I'm still learning about many topics. Could you ask me something else?",
                "I'm not familiar with that specific query. Could you try a different question?"
            ])
                        
    except Exception as e:
        logging.error(f"Error getting response from model: {e}")
    
    # Return None if response generation fails
    # The main app will use a fallback response
    return None

def update_model():
    """
    Update the model with new training data
    """
    train_model()
    return {"success": True, "message": "Model updated successfully"}
