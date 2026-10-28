import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Токен YandexGPT API, который ты указал
YANDEX_API_KEY = "AQVNx434xqWpMO1qcPH8aphP8oWgSAG3OPx6HofL"
# Урл для YandexGPT (используем модель yandexgpt/latest)
YANDEX_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

@app.route('/test', methods=['GET'])
def test_connection():
    return jsonify({"status": "success", "message": "Railway server with Alisa AI is online!"})

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json or {}
    user_text = data.get("text", "Привет")
    print(f"[INFO] Запрос: {user_text}")
    
    # Формируем тело запроса для Яндекса с системным промптом про имя Мира
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }
    
    payload = {
        "modelUri": "gpt://b1g.../yandexgpt/latest", # Замени folder_id если понадобится, либо используем общую структуру
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": 100
        },
        "messages": [
            {
                "role": "system",
                "text": "Твое имя теперь Мира. Ты голосовой ассистент. Отвечай кратко, строго на русском языке, в 1-2 предложения."
            },
            {
                "role": "user",
                "text": user_text
            }
        ]
    }
    
    # ПРИМЕЧАНИЕ: Чтобы не усложнять с folder_id, если у тебя ключ формата Yandex Cloud IAM/Api-Key, 
    # в Яндексе также есть удобный упрощенный ассистентский эндпоинт или стандартная структура.
    # Давай сделаем универсально через стандартный запрос к YandexGPT:
