import psycopg2


class DBManager:

    def __init__(self, dbname: str, params: dict):
        self.dbname = dbname
        self.params = params

    def connect_db(self):
        """ Метод для подключения к бд"""
        conn = psycopg2.connect(dbname=self.dbname, **self.params)
        return conn

    @staticmethod
    def close_connect_db(conn: psycopg2):
        """ Метод для отключения от бд"""
        conn.close()

    def get_companies_and_vacancies_count(self):
        """ Метод для получения списка всех компаний и количество вакансий у каждой компании"""
        conn = self.connect_db()
        with conn.cursor() as cur:
            cur.execute(
                """
            SELECT emp.name, count(*) from employers as emp
            LEFT JOIN vacancies as vac using(employer_id)
            GROUP BY emp.name
            """
            )
            select_data = cur.fetchall()
        self.close_connect_db(conn)
        for current_select_data in select_data:
            print(f"{current_select_data[0]} - {current_select_data[1]} ваканс.")

    def get_all_vacancies(self):
        """ Метод для получения всех вакансий"""
        conn = self.connect_db()
        with conn.cursor() as cur:
            cur.execute(
                """
            SELECT emp.name, vac.name, vac.salary, vac.alternate_url from employers as emp
            LEFT JOIN vacancies as vac using(employer_id)
            """
            )
            select_data = cur.fetchall()
        self.close_connect_db(conn)
        for current_select_data in select_data:
            print(
                f"{current_select_data[0]}, {current_select_data[1]}, зп: {current_select_data[2]}, "
                f"ссылка на вакансию: {current_select_data[3]}"
            )

    def get_avg_salary(self):
        """ Метод для получения средней зп для всех вакансий"""
        conn = self.connect_db()
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT AVG(salary) from vacancies
                    """
            )
            select_data = cur.fetchall()
        self.close_connect_db(conn)
        print(f"Средняя зп по всем вакансиям: {round(select_data[0][0], 3)}")

    def get_vacancies_with_higher_salary(self):
        """ Метод для получения вакансий, у которых зп выше средней"""
        conn = self.connect_db()
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT * from vacancies
                    WHERE salary > (SELECT AVG(salary) from vacancies)
                    """
            )
            select_data = cur.fetchall()
        self.close_connect_db(conn)
        for current_select_data in select_data:
            print(
                f"{current_select_data[2]}, зп: {current_select_data[3]}, "
                f"ссылка на вакансию: {current_select_data[4]}"
            )

    def get_vacancies_with_keyword(self, key_word: str):
        """ Метод для получения вакансий, содержащих в названии ключевое слово"""
        conn = self.connect_db()
        with conn.cursor() as cur:
            cur.execute(
                f"""
                    SELECT * from vacancies
                    WHERE name ILIKE '%{key_word}%'
                    """
            )
            select_data = cur.fetchall()
        self.close_connect_db(conn)
        print(f"Вакансии, содержащие фильтрацию по ключевому слову '{key_word}':")
        for current_select_data in select_data:
            print(
                f"{current_select_data[2]}, зп: {current_select_data[3]}, "
                f"ссылка на вакансию: {current_select_data[4]}"
            )
