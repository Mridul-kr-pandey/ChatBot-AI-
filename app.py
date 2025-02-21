from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Configure Gemini API Key (Stored in .env file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  

if not GEMINI_API_KEY:
    raise ValueError("❌ Missing Gemini API Key. Set it in the .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Sentiment analysis function with emoji feedback
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive 😊"
    elif analysis.sentiment.polarity < 0:
        return "negative 😔"
    else:
        return "neutral 😐"

# Function to book a meeting
def book_meeting(date, time, attendees):
    return {
        "status": "✅ Success",
        "date": date,
        "time": time,
        "attendees": attendees
    }

# Chatbot endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "⚠️ Please enter a message!"}), 400

    sentiment = analyze_sentiment(user_input)
    print(f"User Sentiment: {sentiment}")

    # Generate AI response from Gemini API
    try:
        gemini_response = model.generate_content(user_input).text
    except Exception as e:
        return jsonify({"response": f"🚨 Error generating response: {str(e)}"})

    # Task automation: Meeting booking
    if "book a meeting" in user_input.lower():
        date = "2025-03-10"  # Replace with NLP extraction logic
        time = "10:00 AM"
        attendees = ["user@example.com"]
        booking_response = book_meeting(date, time, attendees)
        return jsonify({"response": f"📅 Meeting booked! Details: {booking_response}"})

    # Modify AI response based on sentiment
    if "negative" in sentiment:
        gemini_response = f"😞 I'm here to help. Let me assist you. {gemini_response}"
    elif "positive" in sentiment:
        gemini_response = f"😊 That's great! Here's something helpful: {gemini_response}"

    return jsonify({"response": gemini_response})

# Serve frontend
@app.route("/")
def home():
    return render_template("index.html")

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
