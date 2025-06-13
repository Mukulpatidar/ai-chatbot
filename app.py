from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# 🔐 Use your actual OpenRouter API key here
API_KEY = "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"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "chatbot",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",  # You can also try `mistralai/mistral-7b-instruct`
        "messages": [{"role": "user", "content": user_input}]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        output = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": output})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))  # 10000 is fallback if PORT not found
    app.run(host="0.0.0.0", port=port, debug=True)
