
import requests
from  datetime import datetime, timedelta
from collections import Counter


class WeatherApp:
    """
    Класс описывает логическую часть программы в приложении в части
    запроса, обработки полученной информации с 'https://openweathermap.org/'
    и вывода ее на экран приложения.
    """

    @staticmethod
    def get_weather(city, self):
        """
        Статический метод класса. Выполняет API-запрос с сайта
        'https://openweathermap.org/'.

        Args:
            city: Город по которому запрашивается погода
            self: Экземпляр класса 'MainWindow' модуля 'gui_modul'.

        Returns:
            При положительном ответе возвращает массив данных в формате
            'json'. Массив передается в другой статический метод класса
            'display_weather' для обработки и вывода на экран приложения
            нужной информации.

            Также из ответа берет информацию о географических
            координатах города (долгота и широта), по которому запрошена
            погода для формирования иного запроса для получения прогноза
            погоды на 3 дня. Данный запрос выполняется в методе
            'get_weather_forecast'.

            В случае возникновения исключений, эти исключения
            обрабатываются и передаются для вывода на экран приложения
            в методе 'weather_error' данного класса.
        """

        #  Публичный ключ.
        api_key = '29cc733366e62c9b6a691e87b96b2f3a'

        # Адрес запроса данных.
        url = (f'https://api.openweathermap.org/data/2.5/weather?q='
               f'{city}&appid={api_key}&units=metric&lang=ru')

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data['cod'] == 200:
                # Вызывается метод для отображения информации на
                # экране приложения..
                WeatherApp.display_weather(data, self)
                lon = data['coord']['lon']
                lat = data['coord']['lat']

                # Вызывается метод для запроса данных в целях получения
                # прогноза погоды на 3 дня.
                WeatherApp.get_weather_forecast(lon, lat, self)

                print(data)  # Вывод в консоль. Для внутр пользования.

        # Обработка ошибок запроса, и вызов метода для отображения
        # ошибки на экране приложения.
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
        """

        Args:
            data: Полученные данные в методе 'get_weather'
            self: Экземпляр класса MainWindow модуля 'gui_modul'.

        Returns:
             Отображает информацию на экране приложения, полученную
        в методе get_weather.
        """
        city_name = data['name']

        # Город сохраняем в файл методом 'save_list_city'
        WeatherApp.save_list_city(city_name)
        self.city_label.setText(f'{city_name}')

        # Перенастройка шрифта, т.к. он может меняться при выводе
        # ошибок при срабатывании метода 'weather_error'.
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

        # Некоторые параметры погоды могут отсутствовать в полученных
        # данных. Поэтому эти ошибки нужно обработать и вывести
        # информацию на экран.
        try:
            visibility_value = int(data['visibility']/1000)
            self.visibility_label.setText(f'Видимость\n   '
                                          f' {visibility_value}км')
        except KeyError:
            self.visibility_label.setText('Видимость недоступна')

        # get_wind_rose - метод для определения направления ветра.
        # Описан ниже.
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
        """
             Статический метод класса. Выполняет API-запрос с сайта
        'https://openweathermap.org/'.

        Args:
            lon: Долгота. Получена в методе get_weather данного класса.
            lat: Широта. Получена в методе get_weather данного класса.
            self: Экземпляр класса 'MainWindow'.

        Returns:
            При положительном ответе возвращает массив данных в формате
            'json'. После обработки полученных данных передает в метод
            'display_weather_forecast' новый массив для отражения на
            экране приложения.

            В случае возникновения исключений, эти исключения
            обрабатываются и передаются для вывода на экран приложения
            в методе 'forecast_error' данного класса
        """

        # Публичный ключ запрашивается на сайте
        # https://openweathermap.org/ после регистрации.
        api_key = '29cc733366e62c9b6a691e87b96b2f3a'
        url = (f'https://api.openweathermap.org/data/2.5/forecast?'
               f'lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ru')

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if int(data['cod']) == 200:

                # На каждый день имеется восемь 3-часовых прогнозов.
                # Их нужно найти в полученном ответе и посчитать
                # среднюю температуру и вероятность погодных условий.
                # Формируются списки на каждый день
                # (температура, описание погоды,код погодных условий).
                # В каждом списке по 8 позиций.
                list_temp_1 = []
                list_description_1 = []
                list_weather_id_1 = []

                list_temp_2 = []
                list_description_2 = []
                list_weather_id_2 = []

                list_temp_3 = []
                list_description_3 = []
                list_weather_id_3 = []

                # Здесь выбираем по ключу ['dt'] в полученных данных
                # только даты ближайших трех дней для включения в
                # списки.
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

                # Новые списки с усредненными значениями температуры,
                # описанием погоды и id.
                forecast_temp = []
                forecast_description = []
                forecast_id = []

                # Средние значения температуры на каждый день добавляем
                # в список
                forecast_temp.append(sum(list_temp_1) / len(list_temp_1))
                forecast_temp.append(sum(list_temp_2) / len(list_temp_2))
                forecast_temp.append(sum(list_temp_3) / len(list_temp_3))

                # Здесь определяются наиболее вероятные сценарии
                # погодных условий на каждый день и так же формируются
                # 2 списка.
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

                # Соотносим данные трех списков по индексу. Формируется
                # список кортежей в формате:
                #                 (температура, описание, id погоды)
                zipped = zip(forecast_temp, forecast_description,
                                 forecast_id)
                final_data = list(zipped)

                print(final_data)  # Для внутреннего пользования

                # Обращаемся к методу 'display_weather_forecast'
                WeatherApp.display_weather_forecast(final_data, self)

        # Обработка ошибок второго запроса. И вывод их на экран
        # приложения с помощью метода 'forecast_error'.
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
        """
            Принимает данные из метода 'get_weather_forecast'
        Args:
            data: Список из трех кортежей в формате:
                (температура, описание погоды, id погодных условий).
            self: Экземпляр класса 'MainWindow'.

        Returns:
            Выводит на экран приложения информацию о прогнозе погоды
            на ближайшие 3 дня.

        """

        # Заполняет информационные виджеты на экране приложения
        # (атрибуты класса MainWindow).

        self.day_1_label.setText(f'{(datetime.now()+
                                     timedelta(days=1)).strftime('%d.%m')}')
        self.day_2_label.setText(f'{(datetime.now()+
                                     timedelta(days=2)).strftime('%d.%m')}')
        self.day_3_label.setText(f'{(datetime.now()+
                                     timedelta(days=3)).strftime('%d.%m')}')


        # get_emoji - статический метод для расшифровки id погоды.
        # Описан ниже
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
        """
            Инициализируется при возникновении ошибок запроса в методе
            'get_weather'.

        Args:
            message: Передается в качестве аргумента из метода
                     get_weather'.

            self: Экземпляр класса 'MainWindow'.

        Returns:
            Сообщение выводится на экран в виджетах
            'temperature_now_label' и 'forecast_label_1'
            класса 'MainWindow'.
            Информация в остальных виджетах стирается.

        """
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
        """
            Инициализируется при возникновении ошибок запроса в методе
            'get_weather_forecast'.
        Args:
            message: Передается в качестве аргумента из метода
            'get_weather_forecast'.
            self: Экземпляр класса 'MainWindow'

        Returns:
            Сообщение выводится на экран в виджете forecast_label_1'
            класса 'MainWindow'.
            Информация в остальных виджетах очищается.

        """
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
        """

        Args:
            city: город.
        Returns:
            Сохраняет в файл город, используется в методе
            display_weather.
        """
        with open('cities.txt', 'a+') as file:
            file.write(f'{city},')

    @staticmethod
    def load_last_city():
        """

        Returns:
            Загружает данные из файла с городами. Используется при
            запуске программы. При отсутствии файла создает новый.
        """
        with open('cities.txt', 'a+') as file:
            file.seek(0)
            string = file.read()
            string = string.replace('\n', '')
            string = string.strip(',')
            list_cities = string.split(',')
            return list_cities[-1]

    @staticmethod
    def get_emoji(weather_id):
        """

        Args:
            weather_id: Код погоды получаемы в ответе на запрос.

        Returns:
            Возвращает вместо кода Эмодзи. Используется в методах
            'display_weather_forecast' и 'display_weather'

        """
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
        """
            Интерпретирует полученную информацию в градусах о
            направлении ветра. Используется в методе 'display_weather'.
        Args:
            wind_deg_value: Значение в градусах.

        Returns:
            Возвращает расшифровку направления ветра.
        """
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

