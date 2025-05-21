from src.work_with_api import HeadHunterAPI, Vacancy
from src.work_with_vacancies import JSONVacancyStorage


api = HeadHunterAPI()
storage = JSONVacancyStorage()

if __name__ == "__main__":
    while True:
        print("\n=== Вакансии с HH.ru ===")
        print("1. Ввести поисковый запрос и сохранить вакансии")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Поиск по ключевому слову в описании")
        print("4. Удалить вакансию по URL")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                query = input("Введите поисковый запрос: ")
                area = int(input("Введите ID региона (например, 113 — Россия, 1 — Москва, 2 — Санкт-Петербург): "))
                per_page = int(input("Сколько вакансий сохранить (макс. 100)? "))
            except ValueError:
                print("Ошибка ввода. Регион и количество должны быть числами.")
                continue

            api = HeadHunterAPI(area=area, per_page=per_page)
            # logger.info("Поиск: %s | Регион: %s | Кол-во: %s", query, area, per_page)

            try:
                vacancies_data = api.get_vacancies(query)
                vacancies = [Vacancy.from_dict(item) for item in vacancies_data]
                for v in vacancies:
                    storage.add_vacancy(v)
                print(f"Сохранено {len(vacancies)} вакансий.")
                # logger.info("Сохранено %s вакансий.", len(vacancies))
            except Exception as e:
                print("Ошибка при получении вакансий:", e)
                # logger.error("Ошибка при получении вакансий: %s", e)
        elif choice == "2":
            try:
                n = int(input("Введите количество вакансий: "))
            except ValueError:
                print("Ошибка: нужно ввести число.")
                continue
            all_vacancies = storage.get_vacancies_by_criteria()
            sorted_vacancies = sorted(all_vacancies, key=lambda v: v.salary or 0, reverse=True)
            top_vacancies = sorted_vacancies[:n]
            print(f"\nТоп-{n} вакансий:")
            for v in top_vacancies:
                print(v)
                print("-" * 40)

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в описании: ").lower()
            results = [
                v for v in storage.get_vacancies_by_criteria()
                if keyword in (v.description or "").lower()
            ]
            if results:
                print(f"\nНайдено {len(results)} вакансий:")
                for v in results:
                    print(v)
                    print("-" * 40)
            else:
                print("Ничего не найдено.")

        elif choice == "4":
            url = input("Введите URL вакансии для удаления: ")
            all_vacancies = storage.get_vacancies_by_criteria()
            to_delete = next((v for v in all_vacancies if v.url == url), None)
            if to_delete:
                storage.delete_vacancy(to_delete)
                print("Вакансия удалена.")
            else:
                print("Вакансия с таким URL не найдена.")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Повторите.")
