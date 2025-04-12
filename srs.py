from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyB3F5gZ7IsHb2rbfvyW1DNdBludpbSCTjs"
genai.configure(api_key=GEMINI_API_KEY)

# Predefined customer support topics and responses
support_topics = {
    "order status": {
        "response": "To check your order status, please visit the 'My Orders' section in your account. If you need help, provide your order number.",
    },
    "return policy": {
        "response": "You can return items within 30 days of delivery. Please ensure the item is in original condition. Visit our Returns Center to start a return.",
    },
    "refund": {
        "response": "Refunds are processed within 5–7 business days after we receive your returned item. You'll get a confirmation once it’s complete.",
    },
    "cancel order": {
        "response": "To cancel your order, go to 'My Orders' and click on 'Cancel Order' next to the item. If it's already shipped, you may need to request a return.",
    },
    "shipping": {
        "response": "Standard shipping takes 3–5 business days. Express options are available at checkout. You’ll get a tracking number once it ships.",
    },
    "technical issue": {
        "response": "Sorry you're facing a technical issue. Could you please describe the problem in more detail so I can assist better?",
    }
}

# Helper: Check if user message matches known topics
def match_support_topic(user_message):
    for keyword, topic in support_topics.items():
        if keyword in user_message.lower():
            return topic
    return None

# Generate response using Gemini or predefined answers
def call_gemini_api(user_message):
    support_response = match_support_topic(user_message)
    if support_response:
        return support_response['response']
    
    # Fallback: Use Gemini for open-ended or unknown queries
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Sorry, I'm having trouble connecting to our support system right now."

@app.route('/')
def index():
    return render_template('index.html')  # Ensure you have this HTML for UI

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    print(f"User message: {user_message}")

    bot_response = call_gemini_api(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
