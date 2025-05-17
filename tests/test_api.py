import pytest
from src.work_with_api import HeadHunterAPI, Vacancy


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


def test_salary_validation():
    vac = Vacancy("Test", "url", None, "desc")
    assert vac.salary == 0

    vac2 = Vacancy("Test", "url", -100, "desc")
    assert vac2.salary == 0

    vac3 = Vacancy("Test", "url", 100000, "desc")
    assert vac3.salary == 100000


def test_comparison():
    vac1 = Vacancy("A", "url", 50000, "desc")
    vac2 = Vacancy("B", "url", 100000, "desc")

    assert vac1 < vac2
    assert vac2 > vac1
    assert vac1 != vac2
    assert vac1 <= vac2
    assert vac2 >= vac1


def test_from_dict_parsing():
    raw_data = {
        "name": "Backend Developer",
        "alternate_url": "https://hh.ru/vacancy/777",
        "salary": {"from": 150000},
        "snippet": {"requirement": "3+ года опыта"}
    }
    vac = Vacancy.from_dict(raw_data)
    assert vac.title == "Backend Developer"
    assert vac.url == "https://hh.ru/vacancy/777"
    assert vac.salary == 150000
    assert "3+ года" in vac.description