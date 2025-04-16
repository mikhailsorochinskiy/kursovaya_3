from src.api import HH
from src.config import config
from src.db_creator import create_database, save_emp_data_to_database, save_vac_data_to_database
from src.dbmanager import DBManager


def main():
    # 1. Загружаем конфигурацию БД
    db_params = config()
    db_name = 'hh_vacancies'

    # 2. Создаем базу данных и таблицы
    print("Создание базы данных...")
    create_database(db_name, db_params)

    # 3. Получаем данные от API HH
    print("\nЗагрузка данных с HeadHunter...")
    hh_api = HH()
    employer_ids = [9694561, 4219, 5919632, 5667343, 9301808, 774144, 10571093, 198614, 6062708, 4306]
    hh_api.load_vacancies(employer_ids)
    hh_api.get_info_employers(employer_ids)

    # 4. Сохраняем данные в БД
    print("\nСохранение данных в базу...")
    db_manager = DBManager(db_name, db_params)
    save_emp_data_to_database(hh_api.employers, db_name, db_params)
    save_vac_data_to_database(hh_api.vacancies, db_name, db_params)

    # 5. Работа с данными через DBManager
    while True:
        print("\nМеню:")
        print("1. Список компаний и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            print("\nКомпании и количество вакансий:")
            db_manager.get_companies_and_vacancies_count()
        elif choice == "2":
            print("\nВсе вакансии:")
            db_manager.get_all_vacancies()
        elif choice == "3":
            db_manager.get_avg_salary()
        elif choice == "4":
            print("\nВакансии с зарплатой выше средней:")
            db_manager.get_vacancies_with_higher_salary()
        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            db_manager.get_vacancies_with_keyword(keyword)
        elif choice == "0":
            print("Выход из программы")
            break
        else:
            print("Неверный ввод, попробуйте снова")


if __name__ == '__main__':
    main()
