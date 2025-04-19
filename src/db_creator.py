import psycopg2


def create_database(database_name: str, params: dict):
    """ Метод для создания бд и таблиц в ней"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
                CREATE TABLE employers (
                    employer_id INT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    description TEXT,
                    alternate_url VARCHAR(255) NOT NULL
                )
            """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
                CREATE TABLE vacancies (
                    vacancy_id INT PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    name VARCHAR(255) NOT NULL,
                    salary INT,
                    alternate_url VARCHAR(255) NOT NULL
                )
            """
        )

    conn.commit()
    conn.close()


def save_emp_data_to_database(data: list[dict], database_name: str, params: dict):
    """ Метод для заполнения данными таблицы employers"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for emp in data:
            cur.execute(
                """
            INSERT INTO employers (employer_id, name, description, alternate_url)
            VALUES (%s, %s, %s, %s)""",
                (emp["id"], emp["name"], emp["description"], emp["alternate_url"]),
            )
    conn.commit()
    conn.close()


def save_vac_data_to_database(data: list[dict], database_name: str, params: dict):
    """ Метод для заполнения данными таблицы vacancies"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vac in data:
            if vac.get("salary") is None or vac.get("salary").get("from") is None:
                cur.execute(
                    """
                INSERT INTO vacancies (vacancy_id, employer_id, name, salary, alternate_url)
                VALUES (%s, %s, %s, %s, %s)""",
                    (vac["id"], vac["employer"]["id"], vac["name"], None, vac["alternate_url"]),
                )
            else:
                cur.execute(
                    """
                INSERT INTO vacancies (vacancy_id, employer_id, name, salary, alternate_url)
                VALUES (%s, %s, %s, %s, %s)""",
                    (
                        vac["id"],
                        vac["employer"]["id"],
                        vac["name"],
                        vac.get("salary").get("from"),
                        vac["alternate_url"],
                    ),
                )
    conn.commit()
    conn.close()
