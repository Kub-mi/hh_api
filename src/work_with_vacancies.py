import json
from abc import ABC, abstractmethod
from typing import Optional, List

from src.work_with_api import Vacancy


class VacancyStorage(ABC):
    """Абстрактный интерфейс хранилища вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies_by_criteria(self, min_salary: Optional[int] = None) -> List[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass


class JSONVacancyStorage(VacancyStorage):
    """Реализация хранилища на базе JSON-файла"""

    def __init__(self, filename: str = "vacancies.json"):
        self.filename = filename

    def _read_file(self) -> List[dict]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: List[dict]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        data = self._read_file()
        data.append({
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description
        })
        self._write_file(data)

    def get_vacancies_by_criteria(self, min_salary: Optional[int] = None) -> List[Vacancy]:
        data = self._read_file()
        result = []
        for item in data:
            if min_salary is None or item["salary"] >= min_salary:
                result.append(Vacancy(**item))
        return result

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        data = self._read_file()
        data = [
            item for item in data
            if not (item["title"] == vacancy.title and item["url"] == vacancy.url)
        ]
        self._write_file(data)
