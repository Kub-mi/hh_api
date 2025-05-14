from abc import ABC, abstractmethod
from typing import List, Dict

import requests


class JobAPI(ABC):
    """
    Абстрактный базовый класс для API-сервисов по вакансиям.
    Обязывает реализовать методы подключения и получения вакансий.
    """

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Получает список вакансий по заданному ключевому слову.
        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список словарей с вакансиями.
        """
        pass


class HeadHunterAPI(JobAPI):
    """
    Класс для подключения и получения вакансий с сайта hh.ru.
    Наследуется от абстрактного класса JobAPI.
    """
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.__per_page = 20

    def __connect(self, keyword: str) -> requests.Response:
        """
        Приватный метод подключения к API hh.ru.
        Отправляет GET-запрос с параметрами.

        :param keyword: Ключевое слово для поиска.
        :return: Объект Response с данными от API.
        """
        params = {
            "text": keyword,
            "area": 113,  # Код России
            "per_page": self.__per_page
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка при запросе к API: {response.status_code}")
        return response

    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Получает список вакансий с сайта hh.ru по ключевому слову.

        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список словарей, каждый из которых содержит данные вакансии.
        """
        response = self.__connect(keyword)
        data = response.json()

        # Возвращаем список вакансий из ответа
        return data.get("items", [])
