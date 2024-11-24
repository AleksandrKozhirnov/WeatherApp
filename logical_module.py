import json

import requests


class WeatherApp:

    @staticmethod
    def get_weather(city, self):
        api_key = '29cc733366e62c9b6a691e87b96b2f3a'

        url = (f'https://api.openweathermap.org/data/2.5/weather?q='
               f'{city}&appid={api_key}&units=metric&lang=ru')

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data['cod'] == 200:
                WeatherApp.display_weather(data, self)
                print(data)

        except requests.exceptions.HTTPError as HTTP_error:
            match response.status_code:
                case 400:
                    WeatherApp.display_error(
                        'Bad Request\nПроверьте, корректность запроса', self)
                case 401:
                    WeatherApp.display_error(
                        'Unauthorized\nAPI-key не действителен/не активен', self)
                case 403:
                    WeatherApp.display_error('Forbidden\nДоступ запрещен', self)
                case 404:
                    WeatherApp.display_error('Not Found\nГород не найден', self)
                case 500:
                    WeatherApp.display_error('Internal Server Error\nПожалуйста, '
                                       'повторите попытку позже', self)
                case 502:
                    WeatherApp.display_error(
                        ' Bad Gateway\nНекорректный ответ от сервера', self)
                case 503:
                    WeatherApp.display_error(
                        'Service Unavailable\nСервер не работает', self)
                case 504:
                    WeatherApp.display_error(
                        'Gateway Timeout\nСервер не отвечает', self)
                case _:
                    WeatherApp.display_error(
                        f'Произошла ошибка HTTP\n{HTTP_error} ', self)


        except requests.exceptions.ConnectionError:
            WeatherApp.display_error(
                f'Connection Error\nПроверьте подключение к сети Интернет.', self)

        except requests.exceptions.Timeout:
            WeatherApp.display_error(f'Timeout Error\nДолгое ожидание ответа.', self)

        except requests.exceptions.TooManyRedirects:
            WeatherApp.display_error(f'Too many Redirects\nПроверь URL.', self)

        except requests.exceptions.RequestException as request_error:
            WeatherApp.display_error(f'Request Error\n{request_error}', self)

    @staticmethod
    def display_weather(data, self):
        city_name = data['name']
        WeatherApp.save_list_city(city_name)
        self.city_label.setText(f'{city_name}')
        self.temperature_now_label.setStyleSheet('font-size: 40px; '
                                           'font-weight: bold')
        temperature_value = data['main']['temp']
        self.temperature_now_label.setText(f'{temperature_value:.0f} C°')
        feeling_value = data['main']['feels_like']
        self.feels_like_label.setText(f'Ощущается как\n'
                                      f'       {feeling_value:.0f} C°')
        weather_id = data['weather'][0]['id']
        self.emoji_label.setText(WeatherApp.get_emoji(weather_id))
        description_value = data['weather'][0]['description']
        self.description_label.setText(f'{description_value.capitalize()}')

        try:
            visibility_value = int(data['visibility']/1000)
            self.visibility_label.setText(f'Видимость\n   '
                                          f' {visibility_value}км')
        except KeyError:
            self.visibility_label.setText('Видимость недоступна')

        try:
            wind_speed_value = data['wind']['speed']
            wind_deg_value = data['wind']['deg']
            self.wind_label.setText(
                f'{wind_speed_value:.0f} м/с\n'
                f'{WeatherApp.get_wind_rose(wind_deg_value)}')
        except KeyError:
            self.wind_label.setText('Информация о ветре\nнедоступна')

        try:
            humidity_value = data['main']['humidity']
            self.humidity_label.setText(f'  💧\n{humidity_value} %')
        except KeyError:
            self.humidity_label.setText('Информация о влажности\n '
                                        'не доступна')

        try:
            pressure_value = data['main']['pressure'] * 0.75
            self.pressure_label.setText(f'   {pressure_value:.0f}\nмм рт.ст.')
        except KeyError:
            self.pressure_label.setText('Информация о давлении\nотсутствует')


    @staticmethod
    def display_error(message, self):
        self.city_label.clear()
        self.temperature_now_label.clear()
        self.feels_like_label.clear()
        self.emoji_label.clear()
        self.description_label.clear()
        self.visibility_label.clear()
        self.humidity_label.clear()
        self.wind_label.clear()
        self.pressure_label.clear()
        self.temperature_now_label.setStyleSheet('font-size: 20px')
        self.temperature_now_label.setText(message)


    @staticmethod
    def save_list_city(city):
        with open('cities.txt', 'a+') as file:
            file.write(f'{city},')

    @staticmethod
    def load_last_city():
        with open('cities.txt', 'a+') as file:
            file.seek(0)
            string = file.read()
            string = string.replace('\n', '')
            string = string.strip(',')
            list_cities = string.split(',')
            return list_cities[-1]

    @staticmethod
    def get_emoji(weather_id):
        if 200 <= weather_id <= 200:
            return '⛈'
        elif 300 <= weather_id <= 321:
            return '🌧'
        elif 500 <= weather_id <= 531:
            return '🌧'
        elif 600 <= weather_id <= 622:
            return '🌨'
        elif 701 <= weather_id <= 781:
            return '🌫'
        elif weather_id == 800:
            return '☀'
        elif 801 <= weather_id <= 803:
            return '🌥'
        elif weather_id == 804:
            return '☁'

    @staticmethod
    def get_wind_rose(wind_deg_value):
        if 337.5 < wind_deg_value <= 360 or 0 <= wind_deg_value < 22.5:
            return 'Северный'
        elif 22.5 <= wind_deg_value < 67.5:
            return 'СВ'
        elif 67.5 <= wind_deg_value < 112.5:
            return 'Восточный'
        elif 112.5 <= wind_deg_value < 157.5:
            return 'ЮВ'
        elif 157.5 <= wind_deg_value < 202.5:
            return 'Южный'
        elif 202.5 <= wind_deg_value < 247.5:
            return 'ЮЗ'
        elif 247.5 <= wind_deg_value < 292.5:
            return 'Западный'
        elif 292.5 <= wind_deg_value <= 337.5:
            return 'СЗ'

