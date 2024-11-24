import sys

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
        self.temperature_now_label = QLabel()
        self.feels_like_label = QLabel()
        self.emoji_label = QLabel()
        self.description_label = QLabel()
        self.visibility_label = QLabel()
        self.humidity_label = QLabel()
        self.wind_label = QLabel()
        self.pressure_label = QLabel()
        self.forecast_label = QLabel('ПРОГНОЗ НА 3 ДНЯ')

        self.init_gui()

    def init_gui(self):

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

        self.set_style()

    def set_style(self):

        self.city_label.setStyleSheet('font-size: 30px')
        self.forecast_label.setStyleSheet('font-size: 30px')
        self.description_label.setStyleSheet('font-size: 20px')
        self.wind_label.setStyleSheet('font-size: 20px')
        self.feels_like_label.setStyleSheet('font-size: 20px')
        self.visibility_label.setStyleSheet('font-size: 20px')
        self.pressure_label.setStyleSheet('font-size: 20px')
        self.emoji_label.setStyleSheet('font-size: 60px; '
                                 'font-family: Segoe UI emoji')
        self.humidity_label.setStyleSheet('font-size: 25px')

        self.click_button()

        WeatherApp.get_weather(WeatherApp.load_last_city(), self)

        self.show()

    def click_button(self):

        self.city_button.clicked.connect(self.get_weather)
        self.city_button.clicked.connect(self.city_input.clear)


    def get_weather(self):
        WeatherApp.get_weather(self.city_input.text(), self)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())






