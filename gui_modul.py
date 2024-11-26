import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit,
                             QLabel, QGridLayout)
from PyQt6.QtCore import Qt

from logical_module import WeatherApp


class MainWindow(QWidget):
    """
    Класс описывает интерфейс погодного приложения.
    """

    def __init__(self):
        """
        Устанавливает виджеты в окне приложения.
        """
        super().__init__()

        self.setWindowTitle('Погода')
        self.empty_label_above_city = QLabel()
        self.city_label = QLabel()
        self.__input_hint = QLabel('Название города')
        self.city_input = QLineEdit()
        self.city_button = QPushButton('Узнать погоду')
        self.refresh_button = QPushButton('ОБНОВИТЬ\nПОГОДУ')
        self.temperature_now_label = QLabel()
        self.feels_like_label = QLabel()
        self.emoji_label = QLabel()
        self.description_label = QLabel()
        self.visibility_label = QLabel()
        self.humidity_label = QLabel()
        self.wind_label = QLabel()
        self.pressure_label = QLabel()
        self.forecast_label = QLabel('ПРОГНОЗ НА 3 ДНЯ')
        self.empty_label_after_forecast_label = QLabel()
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

        self.init_gui()  # Переход к настройке окон

    def init_gui(self):
        """
        Returns:
             Настраивает виджеты. Устанавливает размеры, расположение
        и выравнивание виджетов.
        """
        self.setMinimumSize(700, 700)
        self.refresh_button.setFixedSize(120, 120)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.__input_hint, 0, 2,
                         alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.city_input, 0, 3)
        layout.addWidget(self.city_button, 0, 4,
                         alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.empty_label_above_city, 1, 1)
        layout.addWidget(self.city_label, 2, 1, 1, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.temperature_now_label, 3, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.emoji_label, 3, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description_label, 3, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.wind_label, 3, 3,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feels_like_label, 4, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.humidity_label, 4, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.visibility_label, 4, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.pressure_label, 4, 3,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.empty_label_after_forecast_label, 5, 1, 1, 1)
        layout.addWidget(self.forecast_label, 6, 1, 1, 3)
        layout.addWidget(self.day_1_label, 7, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.day_2_label, 7, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.day_3_label, 7, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_emoji_label_1, 8, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_emoji_label_2, 8, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_emoji_label_3, 8, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.refresh_button, 8, 3,
                         alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.forecast_label_1, 9, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_label_2, 9, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_label_3, 9, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_description_1, 10, 0,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_description_2, 10, 1,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.forecast_description_3, 10, 2,
                         alignment=Qt.AlignmentFlag.AlignCenter)

        self.set_style()  # Переход к настройке шрифтов

    def set_style(self):
        """
        Returns:
            Устанавливает шрифты для виджетов.
        """

        self.city_label.setStyleSheet('font-size: 40px;'
                                      'font-weight: bold')
        self.forecast_label.setStyleSheet('font-size: 30px;'
                                          'font-weight: bold')
        self.description_label.setStyleSheet('font-size: 20px;'
                                             'font-weight: bold')

        self.wind_label.setStyleSheet('font-size: 20px; font-weight: bold')
        self.feels_like_label.setStyleSheet('font-size: 20px;'
                                            'font-weight: bold')

        self.visibility_label.setStyleSheet('font-size: 20px;'
                                            'font-weight: bold')

        self.pressure_label.setStyleSheet('font-size: 20px; font-weight: bold')
        self.emoji_label.setStyleSheet('font-size: 60px; '
                                       'font-family: Segoe UI emoji')

        self.humidity_label.setStyleSheet('font-size: 25px; font-weight: bold')
        self.day_1_label.setStyleSheet('font-size: 25px; font-weight: bold')
        self.day_2_label.setStyleSheet('font-size: 25px; font-weight: bold')
        self.day_3_label.setStyleSheet('font-size: 25px; font-weight: bold')
        self.forecast_emoji_label_1.setStyleSheet('font-size: 50px; '
                                                  'font-family: '
                                                  'Segoe UI emoji')

        self.forecast_emoji_label_2.setStyleSheet('font-size: 50px; '
                                                  'font-family:'
                                                  'Segoe UI emoji')

        self.forecast_emoji_label_3.setStyleSheet('font-size: 50px; '
                                                  'font-family:'
                                                  'Segoe UI emoji')

        self.refresh_button.setStyleSheet('font-size: 20px;')
        self.forecast_label_2.setStyleSheet('font-size: 35px;'
                                            'font-weight: bold')
        self.forecast_label_3.setStyleSheet('font-size: 35px;'
                                            'font-weight: bold')
        self.forecast_description_1.setStyleSheet('font-size: 23px')
        self.forecast_description_2.setStyleSheet('font-size: 23px')
        self.forecast_description_3.setStyleSheet('font-size: 23px')

        # После настройки виджетов, при запуске окна приложения
        # выполняются методы get_weather и 'load_last_city' из модуля
        # 'logical_module.py' класса 'WeatherApp' для загрузки из
        # списка городов, последнего просмотренного при закрытии
        # приложения города и показа погоды по нему.
        WeatherApp.get_weather(WeatherApp.load_last_city(), self)

        self.click_button()  # Переход к привязке кнопочных виджетов/

    def click_button(self):
        """
            Настройка отклика кнопок.
        Returns:
            При нажатии на кнопку 'city_button' происходит выполнение
        'get_weather' и очистка поля ввода запроса 'city_input'.
        """

        self.city_button.clicked.connect(self.get_weather)
        self.city_button.clicked.connect(self.city_input.clear)
        self.refresh_button.clicked.connect(self.refresh_weather)

    def get_weather(self):
        """
           Реализуется при нажатии кнопки city_button.

        Returns:
            Вызывает метод ''get_weather из класса 'WeatherApp' модуля
            'logical_module', который принимает текст из строки поиска
            виджета 'city_input'.

            Так же передает экземпляр класса в качестве аргумента
            в класс WeatherApp в модуле 'logical_module', где
            выполняется логическая часть программы в целях поддержания
            связи с атрибутами данного класса.
        """
        WeatherApp.get_weather(self.city_input.text(), self)

    def refresh_weather(self):
        """
        Returns:
        Вызывает методы 'get_weather' и 'load_last_city' из класса
        'WeatherApp' модуля 'logical_module'

        Так же передает экземпляр класса в качестве аргумента
        в класс WeatherApp в модуле 'logical_module', где выполняется
        логическая часть программы в целях поддержания связи
        с атрибутами данного класса.
        """
        WeatherApp.get_weather(WeatherApp.load_last_city(), self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
