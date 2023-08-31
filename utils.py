import datetime

import psycopg2
import requests


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cur.execute(f"CREATE DATABASE {db_name};")

    cur.close()
    conn.close()


def get_employers(employers_id: list):
    employers = []
    url = 'https://api.hh.ru/employers/'
    for employer_id in employers_id:
        employer = {}
        response = requests.get(url + str(employer_id))
        response_json = response.json()

        employer['company_name'] = response_json['name']
        employer['description'] = response_json['description']
        employer['url'] = response_json['site_url']
        employer['city'] = response_json['area']['name']

        employers.append(employer)
    return employers


def get_vacancies(employer_id: int):
    vacancies = []
    url = 'https://api.hh.ru/vacancies'
    params = {'employer_id': employer_id, 'per_page': 100, 'area': 68}

    response = requests.get(url, params=params)
    response_json = response.json()
    hh_vacancies = response_json.get('items', [])
    for hh_vacancy in hh_vacancies:
        vacancy = {}
        vacancy['job_title'] = hh_vacancy['name']
        vacancy['job_url'] = hh_vacancy['alternate_url']
        if hh_vacancy['salary']:
            vacancy['salary'] = hh_vacancy['salary']['from']
            vacancy['salary_currency'] = hh_vacancy['salary']['currency']
        else:
            vacancy['salary'] = None
            vacancy['salary_currency'] = None
        vacancy['date'] = datetime.datetime.strptime(hh_vacancy['published_at'], '%Y-%m-%dT%H:%M:%S+%f').strftime(
            "%Y-%m-%d")
        vacancy['city'] = hh_vacancy['area']['name']
        vacancy['employer'] = hh_vacancy['employer']['name']
        vacancies.append(vacancy)

    return vacancies


def create_employers_table(cur):
    cur.execute('DROP TABLE IF EXISTS employers')
    cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    company_name TEXT,
                    city VARCHAR(50),
                    url TEXT,
                    description TEXT
                )
            """)


def create_vacancies_table(cur):
    cur.execute("DROP TABLE IF EXISTS vacancies")
    cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    job_title TEXT,
                    job_url TEXT,
                    publication_date DATE,
                    salary INTEGER,
                    salary_currency VARCHAR(5),
                    city VARCHAR(50),
                    employer_id SMALLINT REFERENCES employers(employer_id) NOT NULL
                )
            """)


def insert_data(cur, employers, vacancies):
    key = 1
    for employer in employers:
        query = """
                    INSERT INTO employers (company_name, description, url, city) 
                    VALUES (%s, %s, %s, %s)
                    RETURNING employer_id
                """
        values = (
            employer['company_name'], employer['description'], employer['url'], employer['city']
        )
        cur.execute(query, values)
        employer_id = cur.fetchone()[0]

        insert_vacancies_data(cur, vacancies[key], employer_id)
        key += 1


def insert_vacancies_data(cur, vacancies, employer_id):
    for vacancy in vacancies:
        query = """
                    INSERT INTO vacancies (job_title, job_url, publication_date, salary, salary_currency, city, employer_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        values = (
            vacancy['job_title'], vacancy['job_url'], vacancy['date'], vacancy['salary'], vacancy['salary_currency'],
            vacancy['city'], employer_id
        )
        cur.execute(query, values)
