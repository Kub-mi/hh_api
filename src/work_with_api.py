from abc import ABC, abstractmethod
from http.client import responses
from typing import List, Dict, Optional

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

    def __init__(self, area: int = 113, per_page: int = 20):
        self.__area = area
        self.__per_page = per_page


    def __connect(self, keyword: str) -> requests.Response:
        """
        Приватный метод подключения к API hh.ru.
        Отправляет GET-запрос с параметрами.

        :param keyword: Ключевое слово для поиска.
        :return: Объект Response с данными от API.
        """
        params = {
            "text": keyword,
            "area": self.__area,  # Код России
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


class Vacancy:
    """
    Класс, представляющий вакансию, полученную с hh.ru.
    Поддерживает сравнение по зарплате и валидацию полей
    """

    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: Optional[int], description: str):
        """
        Инициализация экземпляра вакансии.
        """
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def _validate_salary(self, salary: Optional[int]) -> int:
        """
        Приватный метод для валидации зарплаты.
        Если зарплата не указана, устанавливает значение 0.

        :param salary: Зарплата в рублях (int) или None
        :return: Целочисленное значение зарплаты
        """
        if isinstance(salary, int) and salary >= 0:
            return salary
        return 0  # зарплата не указана или некорректная

    # Методы сравнения вакансий по зарплате
    def __lt__(self, other) -> bool:
        return self.salary < other.salary

    def __le__(self, other) -> bool:
        return self.salary <= other.salary

    def __gt__(self, other) -> bool:
        return self.salary > other.salary

    def __ge__(self, other) -> bool:
        return self.salary >= other.salary

    def __eq__(self, other) -> bool:
        return self.salary == other.salary

    def __str__(self) -> str:
        """
        Возвращает строковое представление вакансии.
        """
        return f"{self.title} | {self.salary} руб. | {self.url}"

    def __repr__(self) -> str:
        return f"Vacancy({self.title!r}, {self.url!r}, {self.salary!r}, {self.description!r})"

    @classmethod
    def from_dict(cls, data: dict) -> "Vacancy":
        """
        Создает объект Vacancy из словаря.

        :param data: Словарь с данными вакансии
        :return: Экземпляр Vacancy
        """
        return cls(
            title=data.get("name", "Без названия"),
            url=data.get("alternate_url", ""),
            salary=cls._parse_salary(data.get("salary")),
            description=data.get("snippet", {}).get("requirement", "Описание не указано")
        )

    @staticmethod
    def _parse_salary(salary_data: Optional[dict]) -> Optional[int]:
        """
        Парсит зарплату из словаря. Использует "from" как основную оценку.

        :param salary_data: Словарь с зарплатой (или None)
        :return: Зарплата как число или None
        """
        if salary_data and isinstance(salary_data, dict):
            salary_from = salary_data.get("from")
            if isinstance(salary_from, int):
                return salary_from
        return None
