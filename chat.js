// DOM Elements
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const chatMessages = document.getElementById('chat-messages');
const typingIndicator = document.getElementById('typing-indicator');

// Load chat history when the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    loadChatHistory();
});

// Handle form submission
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Clear input
    messageInput.value = '';
    
    // Display user message
    appendMessage('user', message);
    
    // Show typing indicator
    typingIndicator.style.display = 'block';
    
    // Send message to server
    sendMessage(message);
});

/**
 * Send message to the server
 * @param {string} message - The message to send
 */
function sendMessage(message) {
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Hide typing indicator
        typingIndicator.style.display = 'none';
        
        // Display bot response
        appendMessage('bot', data.response);
    })
    .catch(error => {
        console.error('Error:', error);
        
        // Hide typing indicator
        typingIndicator.style.display = 'none';
        
        // Display error message
        appendMessage('bot', 'Sorry, I encountered an error. Please try again.');
    });
}

/**
 * Append a message to the chat display
 * @param {string} sender - The sender of the message ('user' or 'bot')
 * @param {string} content - The message content
 */
function appendMessage(sender, content) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    
    // Create message bubble with proper styling
    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble');
    bubble.textContent = content;
    
    // Create timestamp
    const timestamp = document.createElement('div');
    timestamp.classList.add('message-timestamp');
    const now = new Date();
    timestamp.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    // Append bubble and timestamp to message container
    messageElement.appendChild(bubble);
    messageElement.appendChild(timestamp);
    
    // Add to chat messages
    chatMessages.appendChild(messageElement);
    
    // Scroll to bottom of chat
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Load chat history from the server
 */
function loadChatHistory() {
    fetch('/history')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.history && data.history.length > 0) {
            // Clear existing messages
            chatMessages.innerHTML = '';
            
            // Add each message to the chat
            data.history.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message', `${message.sender_type}-message`);
                
                // Create message bubble
                const bubble = document.createElement('div');
                bubble.classList.add('message-bubble');
                bubble.textContent = message.content;
                
                // Create timestamp
                const timestamp = document.createElement('div');
                timestamp.classList.add('message-timestamp');
                timestamp.textContent = formatTimestamp(message.timestamp);
                
                // Append bubble and timestamp to message container
                messageElement.appendChild(bubble);
                messageElement.appendChild(timestamp);
                
                // Add to chat messages
                chatMessages.appendChild(messageElement);
            });
            
            // Scroll to bottom of chat
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } else {
            // Add welcome message if no history
            appendMessage('bot', 'Hello! I\'m your intelligent chatbot assistant. How can I help you today?');
        }
    })
    .catch(error => {
        console.error('Error loading chat history:', error);
        appendMessage('bot', 'Hello! I\'m your intelligent chatbot assistant. How can I help you today?');
    });
}

/**
 * Format timestamp for display
 * @param {string} timestamp - The timestamp to format
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
