import os
import pytest


from src.work_with_api import HeadHunterAPI, Vacancy
from src.work_with_vacancies import JSONVacancyStorage

TEST_FILE = "test_vacancies.json"


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


@pytest.fixture
def storage():
    # Удаляем файл перед каждым тестом
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    return JSONVacancyStorage(TEST_FILE)


def test_add_and_get_vacancy(storage):
    vacancy = Vacancy("Python Dev", "http://hh.ru/1", 100000, "Опыт от 2 лет")
    storage.add_vacancy(vacancy)

    results = storage.get_vacancies_by_criteria(min_salary=90000)
    assert len(results) == 1
    assert results[0].title == "Python Dev"


def test_filtering_by_salary(storage):
    storage.add_vacancy(Vacancy("Junior", "url1", 50000, "desc"))
    storage.add_vacancy(Vacancy("Middle", "url2", 100000, "desc"))
    storage.add_vacancy(Vacancy("Senior", "url3", 200000, "desc"))

    results = storage.get_vacancies_by_criteria(min_salary=100000)
    titles = [v.title for v in results]
    assert "Middle" in titles and "Senior" in titles and "Junior" not in titles



def test_deletion(storage):
    vac = Vacancy("To Delete", "url", 100000, "desc")
    storage.add_vacancy(vac)
    storage.delete_vacancy(vac)

    results = storage.get_vacancies_by_criteria()
    assert all(v.title != "To Delete" for v in results)
