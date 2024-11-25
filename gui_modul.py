import sys
from encodings.punycode import adapt

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PyQt6.QtCore import Qt

from logical_module import WeatherApp


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Погода')
        self.setMinimumSize(700, 700)

        self.city_label = QLabel()
        self.__input_hint = QLabel('Название города')
        self.city_input = QLineEdit()
        self.city_button = QPushButton('Узнать погоду')
        self.refresh_button = QPushButton('🔘\nОБНОВИТЬ')
        self.temperature_now_label = QLabel()
        self.feels_like_label = QLabel()
        self.emoji_label = QLabel()
        self.description_label = QLabel()
        self.visibility_label = QLabel()
        self.humidity_label = QLabel()
        self.wind_label = QLabel()
        self.pressure_label = QLabel()
        self.forecast_label = QLabel('ПРОГНОЗ НА 3 ДНЯ')
        self.day_1_label = QLabel()
        self.day_2_label = QLabel()
        self.day_3_label = QLabel()
        self.forecast_emoji_label_1 = QLabel()
        self.forecast_emoji_label_2 = QLabel()
        self.forecast_emoji_label_3 = QLabel()
        self.forecast_label_1 = QLabel()
        self.forecast_label_2 = QLabel()
        self.forecast_label_3 = QLabel()
        self.forecast_description_1 = QLabel()
        self.forecast_description_2 = QLabel()
        self.forecast_description_3 = QLabel()

        self.init_gui()

    def init_gui(self):
        self.refresh_button.setFixedSize(120,120)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.__input_hint, 0, 2,
                         alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.city_input, 0, 3)
        layout.addWidget(self.city_button, 0, 4,
                         alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.city_label, 1, 1,
                         alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.temperature_now_label, 2, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.emoji_label, 2, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description_label, 2, 2)
        layout.addWidget(self.wind_label, 2, 3,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feels_like_label, 3, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.humidity_label, 3, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.visibility_label, 3, 2)
        layout.addWidget(self.pressure_label, 3, 3,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_label, 4, 1)
        layout.addWidget(self.day_1_label, 5, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.day_2_label, 5, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.day_3_label, 5, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_emoji_label_1, 6, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_emoji_label_2, 6, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_emoji_label_3, 6, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.refresh_button, 6, 3,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_label_1, 7, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_label_2, 7, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_label_3, 7, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_description_1, 8, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_description_2, 8, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_description_3, 8, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        self.set_style()

    def set_style(self):

        self.city_label.setStyleSheet('font-size: 40px;'
                                      'font-weight: bold')
        self.forecast_label.setStyleSheet('font-size: 30px')
        self.description_label.setStyleSheet('font-size: 20px')
        self.wind_label.setStyleSheet('font-size: 20px; font-weight: bold')
        self.feels_like_label.setStyleSheet('font-size: 20px')
        self.visibility_label.setStyleSheet('font-size: 20px')
        self.pressure_label.setStyleSheet('font-size: 20px; font-weight: bold')
        self.emoji_label.setStyleSheet('font-size: 60px; '
                                       'font-family: Segoe UI emoji')
        self.humidity_label.setStyleSheet('font-size: 25px; font-weight: bold')
        self.day_1_label.setStyleSheet('font-size: 25px; font-weight: bold')
        self.day_2_label.setStyleSheet('font-size: 25px; font-weight: bold')
        self.day_3_label.setStyleSheet('font-size: 25px; font-weight: bold')
        self.forecast_emoji_label_1.setStyleSheet('font-size: 50px; '
                                 'font-family: Segoe UI emoji')
        self.forecast_emoji_label_2.setStyleSheet('font-size: 50px; '
                                 'font-family: Segoe UI emoji')
        self.forecast_emoji_label_3.setStyleSheet('font-size: 50px; '
                                 'font-family: Segoe UI emoji')
        self.refresh_button.setStyleSheet('font-size: 20px; '
                                 'font-family: Segoe UI emoji')
        self.forecast_label_2.setStyleSheet('font-size: 35px;'
                                            'font-weight: bold')
        self.forecast_label_3.setStyleSheet('font-size: 35px;'
                                            'font-weight: bold')
        self.forecast_description_1.setStyleSheet('font-size: 23px')
        self.forecast_description_2.setStyleSheet('font-size: 23px')
        self.forecast_description_3.setStyleSheet('font-size: 23px')

        WeatherApp.get_weather(WeatherApp.load_last_city(), self)

        self.show()

        self.click_button()

    def click_button(self):

        self.city_button.clicked.connect(self.get_weather)
        self.city_button.clicked.connect(self.city_input.clear)

        self.refresh_button.clicked.connect(self.refresh_weather)

    def get_weather(self):
        WeatherApp.get_weather(self.city_input.text(), self)


    def refresh_weather(self):
        WeatherApp.get_weather(WeatherApp.load_last_city(), self)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())






