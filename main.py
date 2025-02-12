import sys
from unittest import case
import requests 
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
        def __init__(self):
                super().__init__()
                self.cidade_label = QLabel('Insira a cidade: ',self)
                self.cidade_input = QLineEdit(self)
                self.get_weather_button = QPushButton("buscar",self)
                self.temperatura_label = QLabel(self)
                self.imagem_label = QLabel(self)
                self.description_label = QLabel(self)
                self.initUI()

        def initUI(self):
                self.setWindowTitle("Clima App")

                vbox = QVBoxLayout() 

                vbox.addWidget(self.cidade_label)
                vbox.addWidget(self.cidade_input)
                vbox.addWidget(self.get_weather_button)
                vbox.addWidget(self.temperatura_label)
                vbox.addWidget(self.imagem_label)
                vbox.addWidget(self.description_label)

                self.setLayout(vbox)

                self.cidade_label.setAlignment(Qt.AlignCenter)
                self.cidade_input.setAlignment(Qt.AlignCenter)
                self.temperatura_label.setAlignment(Qt.AlignCenter)
                self.imagem_label.setAlignment(Qt.AlignCenter)
                self.description_label.setAlignment(Qt.AlignCenter)


                self.cidade_label.setObjectName("cidade_label")
                self.cidade_input.setObjectName("cidade_input")
                self.get_weather_button.setObjectName("weather_button")
                self.temperatura_label.setObjectName("temperatura_label")
                self.imagem_label.setObjectName("imagem_label")
                self.description_label.setObjectName("description_label")

                
                self.setStyleSheet("""                      
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#cidade_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#cidade_input{
                background-color: #5b586e;
                border-radius: 16px;
                padding: 5px 0;
                border: 1px solid #5b586e;
                color: #fff;
                font-size: 40px;
            }
            #cidade_input:focus{
                background-color: #343155;
                border: 1px solid #8b86aa;
            }
            QPushButton#weather_button{
                color: #fff;
                border: 5px solid #525252;
                border-radius: 8px;
                padding: 1px 5px;
                min-width: 120px;
                min-height:35px;
                font-size: 30px;
                font-weight: bold;
                background-color : #212529;
            }
            #weather_button:hoever{
                background-color : #1c1f23;
            }
            #weather_button:pressed{
                border: 4px solid #a0a2a4;
            }
            QLabel#temperatura_label{
                font-size: 75px;
            }
            QLabel#imagem_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
            "background-color:black;"
                                   
        """)
                self.setAutoFillBackground(True)
                p = self.palette()
                p.setColor(self.backgroundRole(), Qt.gray)
                self.setPalette(p)
                self.get_weather_button.clicked.connect(self.get_weather)
                
        def get_weather(self):
            api_key = "3e64880872002cc52195459020df83ac"
            cidade = self.cidade_input.text()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang={'pt_br'}"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                

                if data["cod"]== 200:
                    self.display_weather(data)
            
            except requests.exceptions.HTTPError as http_error:
                match response.status_code:
                    case 400:
                         self.display_error("Bad request:\nPlease check your input")
                    case 401:
                        self.display_error("Unauthorized:\nInvalid API key")
                    case 403:
                        self.display_error("Forbidden:\nAccess is denied")
                    case 404:
                        self.display_error("Not found:\nCity not found")
                    case 500:
                        self.display_error("Internal Server Error:\nPlease try again later")
                    case 502:
                        self.display_error("Bad Gateway:\nInvalid response from the server")
                    case 503:
                        self.display_error("Service Unavailable:\nServer is down")
                    case 504:
                        self.display_error("Gateway Timeout:\nNo response from the server")
                    case _:
                        self.display_error(f"HTTP error occurred:\n{http_error}")     

            except requests.exceptions.ConnectionError:
                self.display_error("Connection Error:\nCheck your internet connection")
            except requests.exceptions.Timeout:
                self.display_error("Timeout Error:\nThe request timed out")
            except requests.exceptions.TooManyRedirects:
                self.display_error("Too many Redirects:\nCheck the URL")
            except requests.exceptions.RequestException as req_error:
                self.display_error(f"Request Error:\n{req_error}")

        def display_weather(self,data):
            self.temperatura_label.setStyleSheet("font-size: 75px;")
            temperatura_k = data["main"]["temp"]
            temperatura_c = temperatura_k - 273.15
            weather_id = data["weather"][0]["id"]
            weather_description = data["weather"][0]["description"]

            self.temperatura_label.setText(f"{temperatura_c:.0f}°C")
            self.imagem_label.setText(self.get_weather_imagem(weather_id))
            self.description_label.setText(weather_description)

        def display_error(self,message):
            self.temperatura_label.setStyleSheet("font-size: 30px;")
            self.temperatura_label.setText(message)
            self.imagem_label.clear()
            self.description_label.clear()

        @staticmethod
        def get_weather_imagem(weather_id):
            if 200 <= weather_id <= 232:
                 return "⛈"
            elif 300 <= weather_id <= 321:
                return "🌦"
            elif 500 <= weather_id <= 531:
                return "🌧"
            elif 600 <= weather_id <= 622:
                return "❄"
            elif 701 <= weather_id <= 741:
                return "🌫"
            elif weather_id == 762:
                return "🌋"
            elif weather_id == 771:
                return "💨"
            elif weather_id == 781:
                return "🌪"
            elif weather_id == 800:
                return "☀"
            elif 801 <= weather_id <= 804:
                return "☁"
            else:
                return ""
                                
if __name__ == "__main__":
        app = QApplication(sys.argv)
        weather_app = WeatherApp()
        weather_app.show()
        sys.exit(app.exec())
