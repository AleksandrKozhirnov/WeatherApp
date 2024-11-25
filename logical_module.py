
import requests
from  datetime import datetime, timedelta
from collections import Counter


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
                lon = data['coord']['lon']
                lat = data['coord']['lat']
                WeatherApp.get_weather_forecast(lon, lat, self)

                print(data)  # Вывод в консоль.

        except requests.exceptions.HTTPError as HTTP_error:
            match response.status_code:
                case 400:
                    WeatherApp.weather_error(
                        'Bad Request\nПроверьте, корректность запроса', self)
                case 401:
                    WeatherApp.weather_error(
                        'Unauthorized\nAPI-key не действителен/не активен', self)
                case 403:
                    WeatherApp.weather_error('Forbidden\nДоступ запрещен', self)
                case 404:
                    WeatherApp.weather_error('Not Found\nГород не найден', self)
                case 500:
                    WeatherApp.weather_error('Internal Server Error\nПожалуйста, '
                                       'повторите попытку позже', self)
                case 502:
                    WeatherApp.weather_error(
                        ' Bad Gateway\nНекорректный ответ от сервера', self)
                case 503:
                    WeatherApp.weather_error(
                        'Service Unavailable\nСервер не работает', self)
                case 504:
                    WeatherApp.weather_error(
                        'Gateway Timeout\nСервер не отвечает', self)
                case _:
                    WeatherApp.weather_error(
                        f'Произошла ошибка HTTP\n{HTTP_error} ', self)


        except requests.exceptions.ConnectionError:
            WeatherApp.weather_error(
                f'Connection Error\nПроверьте подключение к сети Интернет.', self)

        except requests.exceptions.Timeout:
            WeatherApp.weather_error(f'Timeout Error\nДолгое ожидание ответа.', self)

        except requests.exceptions.TooManyRedirects:
            WeatherApp.weather_error(f'Too many Redirects\nПроверь URL.', self)

        except requests.exceptions.RequestException as request_error:
            WeatherApp.weather_error(f'Request Error\n{request_error}', self)

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
    def get_weather_forecast(lon, lat, self):
        api_key = '29cc733366e62c9b6a691e87b96b2f3a'
        url = (f'https://api.openweathermap.org/data/2.5/forecast?'
               f'lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ru')

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if int(data['cod']) == 200:
                list_temp_1 = []
                list_description_1 = []
                list_weather_id_1 = []

                list_temp_2 = []
                list_description_2 = []
                list_weather_id_2 = []

                list_temp_3 = []
                list_description_3 = []
                list_weather_id_3 = []

                for i in data['list']:
                    if (int(datetime.fromtimestamp(i['dt']).strftime('%d'))
                            == int((datetime.now()+timedelta(days=1)).strftime('%d'))):
                        list_temp_1.append(i['main']['temp'])
                        list_description_1.append(i['weather'][0]['description'])
                        list_weather_id_1.append(i['weather'][0]['id'])


                    elif (int(datetime.fromtimestamp(i['dt']).strftime('%d'))
                            == int((datetime.now()+timedelta(days=2)).strftime('%d'))):
                        list_temp_2.append(i['main']['temp'])
                        list_description_2.append(i['weather'][0]['description'])
                        list_weather_id_2.append(i['weather'][0]['id'])

                    elif (int(datetime.fromtimestamp(i['dt']).strftime('%d'))
                            == int((datetime.now()+timedelta(days=3)).strftime('%d'))):
                        list_temp_3.append(i['main']['temp'])
                        list_description_3.append(i['weather'][0]['description'])
                        list_weather_id_3.append(i['weather'][0]['id'])

                forecast_temp = []
                forecast_description = []
                forecast_id = []

                forecast_temp.append(sum(list_temp_1) / len(list_temp_1))
                forecast_temp.append(sum(list_temp_2) / len(list_temp_2))
                forecast_temp.append(sum(list_temp_3) / len(list_temp_3))

                most_pop_descr_1 = (
                    Counter(list_description_1).most_common(1))[0][0]
                forecast_description.append(most_pop_descr_1)

                most_pop_descr_2 = (
                    Counter(list_description_2).most_common(1))[0][0]
                forecast_description.append(most_pop_descr_2)

                most_pop_descr_3 = (
                    Counter(list_description_3).most_common(1))[0][0]
                forecast_description.append(most_pop_descr_3)

                most_pop_id_1 = (
                    Counter(list_weather_id_1).most_common(1))[0][0]
                forecast_id.append(most_pop_id_1)
                most_pop_id_2 = (
                    Counter(list_weather_id_2).most_common(1))[0][0]
                forecast_id.append(most_pop_id_2)

                most_pop_id_3 = (
                    Counter(list_weather_id_3).most_common(1))[0][0]
                forecast_id.append(most_pop_id_3)

                zipped = zip(forecast_temp, forecast_description,
                                 forecast_id)
                final_data = list(zipped)

                print(final_data)  # Убрать

                WeatherApp.display_weather_forecast(final_data, self)

        except requests.exceptions.HTTPError as HTTP_error:
            match response.status_code:
                case 400:
                    WeatherApp.forecast_error(
                        'Bad Request\nПроверьте, корректность запроса', self)
                case 401:
                    WeatherApp.forecast_error(
                        'Unauthorized\nAPI-key не действителен/не активен',
                        self)
                case 403:
                    WeatherApp.forecast_error('Forbidden\nДоступ запрещен',
                                             self)
                case 404:
                    WeatherApp.forecast_error('Not Found\nГород не найден',
                                             self)
                case 500:
                    WeatherApp.forecast_error(
                        'Internal Server Error\nПожалуйста, '
                        'повторите попытку позже', self)
                case 502:
                    WeatherApp.forecast_error(
                        ' Bad Gateway\nНекорректный ответ от сервера', self)
                case 503:
                    WeatherApp.forecast_error(
                        'Service Unavailable\nСервер не работает', self)
                case 504:
                    WeatherApp.forecast_error(
                        'Gateway Timeout\nСервер не отвечает', self)
                case _:
                    WeatherApp.forecast_error(
                        f'Произошла ошибка HTTP\n{HTTP_error} ', self)


        except requests.exceptions.ConnectionError:
            WeatherApp.forecast_error(
                f'Connection Error\nПроверьте подключение к сети Интернет.',
                self)

        except requests.exceptions.Timeout:
            WeatherApp.forecast_error(f'Timeout Error\nДолгое ожидание ответа.',
                                     self)

        except requests.exceptions.TooManyRedirects:
            WeatherApp.forecast_error(f'Too many Redirects\nПроверь URL.', self)

        except requests.exceptions.RequestException as request_error:
            WeatherApp.forecast_error(f'Request Error\n{request_error}', self)

    @staticmethod
    def display_weather_forecast(data, self):

        self.day_1_label.setText(f'{(datetime.now()+timedelta(days=1)).strftime('%d.%m')}')
        self.day_2_label.setText(f'{(datetime.now()+timedelta(days=2)).strftime('%d.%m')}')
        self.day_3_label.setText(f'{(datetime.now()+timedelta(days=3)).strftime('%d.%m')}')


        emoji_value_1 = WeatherApp.get_emoji(data[0][2])
        self.forecast_emoji_label_1.setText(f'{emoji_value_1}')


        emoji_value_2 = WeatherApp.get_emoji(data[1][2])
        self.forecast_emoji_label_2.setText(f'{emoji_value_2}')

        emoji_value_3 = WeatherApp.get_emoji(data[2][2])
        self.forecast_emoji_label_3.setText(f'{emoji_value_3}')

        temp_value_1 = data[0][0]
        self.forecast_label_1.setStyleSheet('font-size: 35px;'
                                            'font-weight: bold')
        self.forecast_label_1.setText(f'  {temp_value_1:.0f} C°')

        temp_value_2 = data[1][0]
        self.forecast_label_2.setText(f'  {temp_value_2:.0f} C°')

        temp_value_3 = data[2][0]
        self.forecast_label_3.setText(f'  {temp_value_3:.0f} C°')

        descr_value_1 = data[0][1]
        self.forecast_description_1.setText(f'{descr_value_1.capitalize()}')

        descr_value_2 = data[1][1]
        self.forecast_description_2.setText(f'{descr_value_2.capitalize()}')

        descr_value_3 = data[2][1]
        self.forecast_description_3.setText(f'{descr_value_3.capitalize()}')


    @staticmethod
    def weather_error(message, self):
        self.city_label.clear()
        self.temperature_now_label.clear()
        self.feels_like_label.clear()
        self.emoji_label.clear()
        self.description_label.clear()
        self.visibility_label.clear()
        self.humidity_label.clear()
        self.wind_label.clear()
        self.pressure_label.clear()
        self.forecast_emoji_label_1.clear()
        self.forecast_emoji_label_2.clear()
        self.forecast_emoji_label_3.clear()
        self.forecast_label_1.clear()
        self.forecast_label_2.clear()
        self.forecast_label_3.clear()
        self.forecast_description_1.clear()
        self.forecast_description_2.clear()
        self.forecast_description_3.clear()
        self.temperature_now_label.setStyleSheet('font-size: 20px')
        self.forecast_label_1.setStyleSheet('font-size: 20px')
        self.temperature_now_label.setText(message)
        self.forecast_label_1.setText(message)

    @staticmethod
    def forecast_error(message, self):
        self.forecast_emoji_label_1.clear()
        self.forecast_emoji_label_2.clear()
        self.forecast_emoji_label_3.clear()
        self.forecast_label_1.setStyleSheet('font-size: 20px')
        self.forecast_label_2.clear()
        self.forecast_label_3.clear()
        self.forecast_description_1.clear()
        self.forecast_description_2.clear()
        self.forecast_description_3.clear()
        self.forecast_label_1.setText(message)


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

    @staticmethod
    def get_date(dt):
        return datetime.fromtimestamp(dt).strftime('%d')