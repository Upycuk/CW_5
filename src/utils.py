import requests
import psycopg2
from typing import Any

employer_ids = [
    '3127',
    '3776',
    '1122462',
    '2180',
    '87021',
    '1740',
    '80',
    '4181',
    '15478',
    '78638'
]


def __get_employee_data() -> list[dict]:
    """
    функция для получения данных о компаниях с сайта HH.ru
    :return: список компаний.
    """
    employers = []
    for employer_id in employer_ids:
        url_emp = f"https://api.hh.ru/employers/{employer_id}"
        employer_info = requests.get(url_emp, ).json()
        employers.append(employer_info)

    return employers


def __get_vacancies_data() -> list:
    """
    функция для получения данных о вакансиях с сайта HH.ru
    :return: список вакансий.
    """
    vacancy = []
    for employer_id in employer_ids:
        url_vac = f"https://api.hh.ru/vacancies/"
        vacancy_info = requests.get(url_vac, params={'page': 0, 'per_page': 100, 'employer_id': employer_id}).json()['items']
        vacancy.extend(vacancy_info)
    return vacancy


def create_database(database_name: str, params: dict) -> None:
    """
    функция для создания Базы Данных и создания таблиц в БД.
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""            
            CREATE TABLE employers (                
                employer_id INTEGER PRIMARY KEY,
                employer_name text not null,
                employer_area TEXT not null,
                employer_url TEXT,
                open_vacancies INTEGER
            );
        """)

    with conn.cursor() as cur:
        cur.execute("""             
            CREATE TABLE vacancy (                
                vacancy_id INTEGER PRIMARY KEY,
                vacancy_name VARCHAR,
                vacancy_area VARCHAR,
                salary INTEGER,
                employer_id INTEGER REFERENCES employers(employer_id) ON UPDATE CASCADE,
                vacancy_url VARCHAR                
            );
        """)

    conn.commit()
    conn.close()


def save_data_to_database_emp(data_emp: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Функция для заполнения таблицы компаний в БД.
    """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for emp in data_emp:
            cur.execute("""
                INSERT INTO employers (employer_id, employer_name, employer_area, employer_url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                """,
                        (emp['id'], emp['name'], emp['area']['name'], emp['alternate_url'], emp['open_vacancies']))

    conn.commit()
    conn.close()


def save_data_to_database_vac(data_vac: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Функция для заполнения таблицы вакансий в БД.
    """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vac in data_vac:
            if vac['salary'] is None or vac['salary']['from'] is None:
                cur.execute("""
                   INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """,
                            (vac.get('id'), vac['name'], vac['area']['name'], 0, vac['employer']['id'],
                             vac['alternate_url']))
            else:
                cur.execute("""
                    INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                            (vac.get('id'), vac['name'], vac['area']['name'], vac['salary']['from'],
                             vac['employer']['id'], vac['alternate_url']))

    conn.commit()
    conn.close()
