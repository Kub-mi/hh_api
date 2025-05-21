import os

import pytest

from src.work_with_api import Vacancy
from src.work_with_vacancies import JSONVacancyStorage

TEST_FILE = "test_vacancies.json"


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
