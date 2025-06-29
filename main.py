from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

app = Flask(__name__)
run_with_ngrok(app)  # Initialize ngrok

# Chatbot responses
responses = {
    "greet": ["Hello!", "Hi there!", "Hey!"],
    "bye": ["Goodbye!", "See you later!", "Bye!"],
    "thanks": ["You're welcome!", "No problem!", "Happy to help!"],
    "default": ["I'm not sure.", "Could you rephrase that?", "Tell me more."]
}

lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

def get_intent(user_input):
    lemmas = preprocess(user_input)
    if any(word in lemmas for word in ["hi", "hello", "hey"]):
        return "greet"
    elif any(word in lemmas for word in ["bye", "goodbye"]):
        return "bye"
    elif any(word in lemmas for word in ["thank", "thanks"]):
        return "thanks"
    return "default"

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Colab Chatbot</title>
        <style>
            body { font-family: Arial; max-width: 600px; margin: 20px auto; padding: 20px; }
            #chatbox { border: 1px solid #ccc; height: 300px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
            #user_input { width: 70%; padding: 8px; }
            button { padding: 8px 15px; background: #4CAF50; color: white; border: none; }
            .user { color: blue; margin: 5px 0; }
            .bot { color: green; margin: 5px 0; }
        </style>
    </head>
    <body>
        <h1>Flask Chatbot in Colab</h1>
        <div id="chatbox"></div>
        <input type="text" id="user_input" placeholder="Type here..." onkeypress="if(event.keyCode==13) sendMessage()">
        <button onclick="sendMessage()">Send</button>

        <script>
            function sendMessage() {
                const input = document.getElementById("user_input").value;
                if (!input.trim()) return;

                const chatbox = document.getElementById("chatbox");
                chatbox.innerHTML += `<div class="user"><b>You:</b> ${input}</div>`;
                document.getElementById("user_input").value = "";

                fetch("/get_response", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: `user_input=${encodeURIComponent(input)}`
                })
                .then(response => response.json())
                .then(data => {
                    chatbox.innerHTML += `<div class="bot"><b>Bot:</b> ${data.response}</div>`;
                    chatbox.scrollTop = chatbox.scrollHeight;
                })
                .catch(error => console.log('Error:', error));
            }
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