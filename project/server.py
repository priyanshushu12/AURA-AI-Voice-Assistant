from flask import Flask, request, jsonify
import main  # Import chatbot logic from main.py

app = Flask(__name__)

# Define API route for chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()  # Get JSON data from request
    user_message = data.get("message", "")

    # Call the chatbot function from main.py
    response = main.generate_response(user_message)

    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
