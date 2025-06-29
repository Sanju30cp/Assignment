from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)

app = Flask(__name__)
run_with_ngrok(app)  # Initialize ngrok

# Enhanced chatbot responses with more functionality
responses = {
    "greet": ["Hello! I'm your AI assistant. How can I help you today?", "Hi there! What can I do for you?", "Hey! Ask me anything - I'm here to help!"],
    "bye": ["Goodbye! Have a great day!", "See you later! Feel free to come back anytime!", "Bye! Thanks for chatting with me!"],
    "thanks": ["You're very welcome!", "No problem at all!", "Happy to help! Anything else you need?"],
    "help": ["I can help you with general questions, provide information, or just have a conversation. What would you like to know?", "I'm here to assist! Try asking me about topics like weather, technology, or general knowledge.", "Feel free to ask me anything - I'll do my best to help!"],
    "weather": ["I don't have access to current weather data, but you can check your local weather service for accurate forecasts!", "For real-time weather information, I'd recommend checking a weather app or website in your area."],
    "time": ["I don't have access to current time data, but you can check your device's clock or search online for the current time in your location."],
    "joke": ["Why don't scientists trust atoms? Because they make up everything!", "What do you call a bear with no teeth? A gummy bear!", "Why did the scarecrow win an award? Because he was outstanding in his field!"],
    "compliment": ["Thank you so much! You're very kind!", "That's really nice of you to say!", "I appreciate the kind words!"],
    "name": ["I'm your AI chatbot assistant! You can call me whatever you'd like.", "I'm an AI assistant created to help and chat with you!", "I'm your friendly AI helper!"],
    "capabilities": ["I can have conversations, answer questions, tell jokes, and provide general information. What would you like to explore?", "I'm designed to be helpful, harmless, and honest. I can chat about various topics and try to assist with your questions!"],
    "default": ["That's interesting! Tell me more.", "I'm not sure about that specific topic. Could you rephrase or ask something else?", "Hmm, I'd love to learn more about what you're thinking. Can you elaborate?", "That's a good question! While I might not have all the answers, I'm happy to discuss it further."]
}

lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

def get_intent(user_input):
    lemmas = preprocess(user_input)
    text_lower = user_input.lower()
    
    # Greeting patterns
    if any(word in lemmas for word in ["hi", "hello", "hey", "greetings"]):
        return "greet"
    
    # Farewell patterns
    elif any(word in lemmas for word in ["bye", "goodbye", "farewell", "see", "later"]):
        return "bye"
    
    # Thanks patterns
    elif any(word in lemmas for word in ["thank", "thanks", "appreciate"]):
        return "thanks"
    
    # Help patterns
    elif any(word in lemmas for word in ["help", "assist", "support"]) or "what can you do" in text_lower:
        return "help"
    
    # Weather patterns
    elif any(word in lemmas for word in ["weather", "temperature", "rain", "sunny", "cloudy"]):
        return "weather"
    
    # Time patterns
    elif any(word in lemmas for word in ["time", "clock", "hour", "minute"]) or "what time" in text_lower:
        return "time"
    
    # Joke patterns
    elif any(word in lemmas for word in ["joke", "funny", "laugh"]) or "tell me a joke" in text_lower:
        return "joke"
    
    # Compliment patterns
    elif any(word in lemmas for word in ["good", "great", "awesome", "amazing", "wonderful", "nice", "smart", "clever"]):
        return "compliment"
    
    # Name/identity patterns
    elif any(phrase in text_lower for phrase in ["what is your name", "who are you", "your name"]):
        return "name"
    
    # Capabilities patterns
    elif any(phrase in text_lower for phrase in ["what can you do", "your capabilities", "what are you capable of"]):
        return "capabilities"
    
    return "default"

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Chatbot Assistant</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 800px;
                height: 600px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 20px 20px 0 0;
            }
            
            .header h1 {
                font-size: 24px;
                margin-bottom: 5px;
            }
            
            .header p {
                opacity: 0.9;
                font-size: 14px;
            }
            
            #chatbox {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f8f9fa;
                scroll-behavior: smooth;
            }
            
            .message {
                margin-bottom: 15px;
                display: flex;
                align-items: flex-start;
            }
            
            .user-message {
                justify-content: flex-end;
            }
            
            .message-content {
                max-width: 70%;
                padding: 12px 16px;
                border-radius: 18px;
                word-wrap: break-word;
                animation: fadeIn 0.3s ease-in;
            }
            
            .user .message-content {
                background: #007bff;
                color: white;
                border-bottom-right-radius: 4px;
            }
            
            .bot .message-content {
                background: white;
                color: #333;
                border: 1px solid #e0e0e0;
                border-bottom-left-radius: 4px;
            }
            
            .input-container {
                padding: 20px;
                background: white;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            #user_input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s ease;
            }
            
            #user_input:focus {
                border-color: #4CAF50;
            }
            
            .send-btn {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 50%;
                width: 45px;
                height: 45px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background-color 0.3s ease, transform 0.1s ease;
                font-size: 18px;
            }
            
            .send-btn:hover {
                background: #45a049;
                transform: scale(1.05);
            }
            
            .send-btn:active {
                transform: scale(0.95);
            }
            
            .typing-indicator {
                display: none;
                margin-bottom: 15px;
            }
            
            .typing-dots {
                background: white;
                border: 1px solid #e0e0e0;
                padding: 12px 16px;
                border-radius: 18px;
                border-bottom-left-radius: 4px;
                max-width: 70px;
            }
            
            .typing-dots span {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #999;
                margin: 0 2px;
                animation: typing 1.4s infinite;
            }
            
            .typing-dots span:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-dots span:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.5;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Mobile responsiveness */
            @media (max-width: 768px) {
                body {
                    padding: 10px;
                }
                
                .container {
                    height: 100vh;
                    border-radius: 0;
                }
                
                .header {
                    border-radius: 0;
                }
                
                .header h1 {
                    font-size: 20px;
                }
                
                .message-content {
                    max-width: 85%;
                }
                
                #user_input {
                    font-size: 16px; /* Prevents zoom on iOS */
                }
            }
            
            @media (max-width: 480px) {
                .header {
                    padding: 15px;
                }
                
                .input-container {
                    padding: 15px;
                }
                
                .message-content {
                    max-width: 90%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Chatbot Assistant</h1>
                <p>Ask me anything! I'm here to help and chat.</p>
            </div>
            
            <div id="chatbox">
                <div class="message bot">
                    <div class="message-content">
                        Welcome! I'm your AI assistant. Try asking me about anything - I can help with questions, tell jokes, or just have a friendly conversation! 😊
                    </div>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            
            <div class="input-container">
                <input type="text" id="user_input" placeholder="Type your message here..." onkeypress="if(event.keyCode==13) sendMessage()">
                <button class="send-btn" onclick="sendMessage()">➤</button>
            </div>
        </div>

        <script>
            function sendMessage() {
                const input = document.getElementById("user_input");
                const message = input.value.trim();
                if (!message) return;

                const chatbox = document.getElementById("chatbox");
                const typingIndicator = document.getElementById("typingIndicator");
                
                // Add user message
                chatbox.innerHTML += `
                    <div class="message user user-message">
                        <div class="message-content">${message}</div>
                    </div>
                `;
                
                input.value = "";
                chatbox.scrollTop = chatbox.scrollHeight;
                
                // Show typing indicator
                typingIndicator.style.display = 'block';
                chatbox.scrollTop = chatbox.scrollHeight;

                fetch("/get_response", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: `user_input=${encodeURIComponent(message)}`
                })
                .then(response => response.json())
                .then(data => {
                    // Hide typing indicator
                    typingIndicator.style.display = 'none';
                    
                    // Add bot response
                    chatbox.innerHTML += `
                        <div class="message bot">
                            <div class="message-content">${data.response}</div>
                        </div>
                    `;
                    chatbox.scrollTop = chatbox.scrollHeight;
                })
                .catch(error => {
                    typingIndicator.style.display = 'none';
                    chatbox.innerHTML += `
                        <div class="message bot">
                            <div class="message-content">Sorry, I'm having trouble responding right now. Please try again!</div>
                        </div>
                    `;
                    chatbox.scrollTop = chatbox.scrollHeight;
                    console.log('Error:', error);
                });
                
                // Focus back on input
                input.focus();
            }
            
            // Auto-focus on input when page loads
            document.addEventListener('DOMContentLoaded', function() {
                document.getElementById('user_input').focus();
            });
        </script>
    </body>
    </html>
    """

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    intent = get_intent(user_input)
    return jsonify({"response": random.choice(responses[intent])})

# Suppress Flask and Werkzeug logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == "__main__":
    print("Starting server...")
    app.run()