#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ПКС";
const char* password = "26102011";

WebServer server(80);

// Код веб-страницы, которая откроется на вашем телефоне или ПК
void handleRoot() {
  String html = "<html><head><meta charset='UTF-8'>";
  html += "<style>body{font-family:Arial; text-align:center; margin-top:50px; background:#f0f2f5;} ";
  html += "h1{color:#1a73e8;} .card{background:white; padding:30px; display:inline-block; border-radius:10px; box-shadow:0 4px 6px rgba(0,0,0,0.1);}</style>";
  html += "</head><body><div class='card'>";
  html += "<h1>Умная колонка Мира</h1>";
  html += "<p>Плата ESP32-D успешно подключена к вашей домашней сети!</p>";
  html += "<p>Связь с сервером ПК работает стабильно.</p>";
  html += "</div></body></html>";
  server.send(200, "text/html", html);
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n--- СТАРТ СИСТЕМЫ ---");

  WiFi.begin(ssid, password);
  Serial.print("Подключение к Wi-Fi: ПКС");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n[УСПЕХ] Wi-Fi подключен!");
  Serial.print("IP-адрес платы в роутере: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.begin();
  Serial.println("Веб-страница запущена и ждет подключений.");
}

void loop() {
  server.handleClient();
}
