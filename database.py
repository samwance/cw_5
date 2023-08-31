import psycopg2


class DBManager:
    def __init__(self, params):
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("""SELECT e.company_name, COUNT(v.vacancy_id) FROM employers AS e
        INNER JOIN vacancies AS v
        USING (employer_id)
        GROUP BY employer_id
        ORDER BY e.company_name""")
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute("""SELECT e.company_name, v.job_title, v.salary, v.job_url FROM vacancies v
        INNER JOIN employers e
        USING (employer_id)""")
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("SELECT CEILING(AVG(salary)) FROM vacancies")
        return self.cur.fetchall()[0][0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute(f"SELECT job_title FROM vacancies WHERE salary > {avg_salary}")
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute(f"SELECT job_title FROM vacancies WHERE job_title LIKE '%{keyword}%'")
        return self.cur.fetchall()

    def close_con(self):
        self.cur.close()
        self.conn.close()