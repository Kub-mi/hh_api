import pytest
from src.work_with_api import HeadHunterAPI

def test_get_vacancies_returns_list():
    """Проверяет, что метод get_vacancies возвращает список с элементами-словарями."""
    hh = HeadHunterAPI()
    vacancies = hh.get_vacancies("Python")
    assert isinstance(vacancies, list)
    assert len(vacancies) > 0
    assert isinstance(vacancies[0], dict)


def test_get_vacancies_filters_by_text():
    """Проверяет, что вакансии содержат ключевое слово в названии или описании."""
    hh = HeadHunterAPI()
    keyword = "Django"
    vacancies = hh.get_vacancies(keyword)
    assert any(keyword.lower() in str(vac["name"]).lower() for vac in vacancies)