from src.api import HH
from src.config import config
from src.db_creator import create_database, save_emp_data_to_database, save_vac_data_to_database
from src.dbmanager import DBManager

employer_ids = [9694561, 4219, 5919632, 5667343, 9301808, 774144, 10571093, 198614, 6062708, 4306]


def main():
    hh = HH()
    hh.load_vacancies(employer_ids)
    hh.get_info_employers(employer_ids)
    params = config()
    create_database('hh_db', params)
    save_emp_data_to_database(hh.employers, 'hh_db', params)
    save_vac_data_to_database(hh.vacancies, 'hh_db', params)
    hh_db = DBManager('hh_db', params)
    hh_db.get_companies_and_vacancies_count()
    hh_db.get_all_vacancies()
    hh_db.get_avg_salary()
    hh_db.get_vacancies_with_higher_salary()
    hh_db.get_vacancies_with_keyword('Менеджер')


if __name__ == '__main__':
    main()
