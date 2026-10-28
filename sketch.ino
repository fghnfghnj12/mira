
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "ПКС";
const char* password = "26102011";
const char* serverUrl = "http://192.168.31.19";

#define TEST_PIN 13

void setup() {
  Serial.begin(115200);
  pinMode(TEST_PIN, INPUT_PULLUP);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[Wi-Fi] Успешно подключено к ПКС!");
}

void loop() {
  if (digitalRead(TEST_PIN) == LOW) {
    Serial.println("Пин 13 замкнут на GND! Отправляю тестовый запрос на сервер ПК...");

    HTTPClient http;
    http.begin(serverUrl);
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      Serial.print("Ответ от сервера получен, код: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Ошибка HTTP-запроса: ");
      Serial.println(httpResponseCode);
    }
    http.end();
    delay(2000); 
  }
}
