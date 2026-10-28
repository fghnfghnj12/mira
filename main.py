import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Твои данные от Yandex Cloud
YANDEX_API_KEY = "AQVNx434xqWpMO1qcPH8aphP8oWgSAG3OPx6HofL"
# ⚠️ Вставь сюда ID твоего каталога (folder_id) из Yandex Cloud (например: "b1gs5... ")
YANDEX_FOLDER_ID = "b1gqeovk5glv70vu879n" 

YANDEX_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

@app.route('/test', methods=['GET'])
def test_connection():
    return jsonify({"status": "success", "message": "Yandex Alisa backend on Railway is online!"})

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json or {}
    user_text = data.get("text", "Привет")
    print(f"[INFO] Запрос к Алисе: {user_text}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }
    
    # Формируем запрос строго по документации YandexGPT
    payload = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.4,
            "maxTokens": 150
        },
        "messages": [
            {
                "role": "system",
                "text": "Твое имя Мира. Ты умная домашняя колонка и голосовой ассистент. Отвечай кратко, строго на русском языке, в 1-2 предложения, без лишней «воды»."
            },
            {
                "role": "user",
                "text": user_text
            }
        ]
    }
    
    try:
        response = requests.post(YANDEX_URL, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            res_data = response.json()
            # Достаем текст ответа из структуры YandexGPT
            answer = res_data["result"]["alternatives"][0]["message"]["text"].strip()
            print(f"[INFO] Ответ от Алисы (Миры): {answer}")
            return jsonify({"status": "success", "answer": answer})
        else:
            print(f"[ERROR] Ошибка от Яндекса: {response.status_code} - {response.text}")
            return jsonify({"status": "error", "message": f"Yandex API error: {response.status_code}"}), 500
            
    except Exception as e:
        print(f"[ERROR] Исключение: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
