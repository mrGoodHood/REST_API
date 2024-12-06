import os
import psycopg2
from psycopg2.extras import DictCursor

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class DatabaseManager:
    def __init__(self):
        self.host = os.getenv('FSTR_DB_HOST')
        self.port = os.getenv('FSTR_DB_PORT')
        self.login = os.getenv('FSTR_DB_LOGIN')
        self.password = os.getenv('FSTR_DB_PASS')
        self.connection = None

    def connect(self):
        """Установление соединения с базой данных"""
        try:
            self.connection = psycopg2.connect(host=self.host, port=self.port, user=self.login, password=self.password, sslmode='require')
            print("Connection to the PostgreSQL established successfully.")
        except Exception as error:
            print("Error while connecting to PostgreSQL:", error)

    def close_connection(self):
        """Закрытие соединения с базой данных"""
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection is closed")

    def execute_query(self, query, values=None):
        """
        Выполнение SQL-запросов
        :param query: SQL-запрос
        :param values: Параметры для подстановки в запрос
        :return: Результат выполнения запроса
        """
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as error:
            print("Error executing query:", error)
            return None

    def insert_user(self, email, fam, name, otc, phone):
        """
        Добавление нового пользователя в таблицу users
        :param email: Email пользователя
        :param fam: Фамилия
        :param name: Имя
        :param otc: Отчество
        :param phone: Телефон
        :return: ID добавленного пользователя
        """
        query = "INSERT INTO users (email, fam, name, otc, phone) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
        values = (email, fam, name, otc, phone)
        result = self.execute_query(query, values)
        return result[0]['id'] if result else None

    def insert_coords(self, latitude, longitude, height):
        """
        Добавление новых координат в таблицу coords
        :param latitude: Широта
        :param longitude: Долгота
        :param height: Высота
        :return: ID добавленных координат
        """
        query = "INSERT INTO coords (latitude, longitude, height) VALUES (%s, %s, %s) RETURNING id;"
        values = (latitude, longitude, height)
        result = self.execute_query(query, values)
        return result[0]['id'] if result else None

    def insert_pereval_added(self, beauty_title, title, other_titles, connect, add_time, user_id, coord_id, winter_level, summer_level, autumn_level, spring_level):
        """
        Добавление нового перевала в таблицу pereval_added
        :param beauty_title: Красивое название перевала
        :param title: Название перевала
        :param other_titles: Другие названия
        :param connect: Что соединяет
        :param add_time: Время добавления
        :param user_id: ID пользователя
        :param coord_id: ID координат
        :param winter_level: Уровень сложности зимой
        :param summer_level: Уровень сложности летом
        :param autumn_level: Уровень сложности осенью
        :param spring_level: Уровень сложности весной
        :return: ID добавленного перевала
        """
        query = "INSERT INTO pereval_added (beauty_title, title, other_titles, connect, add_time, user_id, coord_id, winter_level, summer_level, autumn_level, spring_level, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'new') RETURNING id;"
        values = (beauty_title, title, other_titles, connect, add_time, user_id, coord_id, winter_level, summer_level, autumn_level, spring_level)
        result = self.execute_query(query, values)
        return result[0]['id'] if result else None

    def insert_image(self, pereval_id, image_data, title):
        """
        Добавление нового изображения в таблицу pereval_images
        :param pereval_id: ID перевала
        :param image_data: Данные изображения
        :param title: Заголовок изображения
        :return: ID добавленного изображения
        """
        query = "INSERT INTO pereval_images (pereval_id, image_data, title) VALUES (%s, %s, %s) RETURNING id;"
        values = (pereval_id, image_data, title)
        result = self.execute_query(query, values)
        return result[0]['id'] if result else None