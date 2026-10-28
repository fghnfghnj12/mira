import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

POLLINATIONS_URL = "https://text.pollinations.ai/"


@app.route('/test', methods=['GET'])
def test_connection():
    return jsonify({"status": "success", "message": "Railway server is online!"})


@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json or {}
    user_text = data.get("text", "Привет")
    print(f"[INFO] Запрос: {user_text}")

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Ты краткий голосовой ассистент. Отвечай строго на русском языке, без эмодзи, без разметки markdown, в 1-2 коротких предложения."
            },
            {"role": "user", "content": user_text}
        ],
        "model": "openai"
    }

    try:
        response = requests.post(POLLINATIONS_URL, json=payload, timeout=15)
        if response.status_code == 200:
            answer = response.text.strip()
            print(f"[INFO] Ответ ИИ: {answer}")
            return jsonify({"status": "success", "answer": answer})
        else:
            print(f"[ERROR] Ошибка API: {response.status_code}")
            return jsonify({"status": "error", "message": f"HTTP {response.status_code}"}), 500
    except Exception as e:
        print(f"[ERROR] Исключение: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)