import sqlite3
import os


class DB:
    def __init__(self):
        """
        initialise dabase connection variable
        """
        self.con = None

    def __enter__(self):
        """
        connect to the database inside a WITH loop
        :return: self
        """
        self.con = sqlite3.connect("db/people.db")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Close connection when exiting the WITH loop
        :param exc_type:
        :param exc_value:
        :param exc_traceback:
        :return:
        """
        self.con.close()

    def create_table_people(self):
        cur = self.con.cursor()
        try:
            cur.execute(
                """CREATE TABLE people (
                    name  varchar(255) NOT NULL,
                    email varchar(255) PRIMARY KEY,
                    street varchar(255),
                    number INTEGER,
                    city varchar(255),
                    state varchar(255) CHECK(state IN ('New South Wales','Victoria','Queensland','South Australia',
                                                       'Western Australia','Northern Territories',
                                                       'Capital Territories'))
                )"""
            )
            self._insert_fake_data()
        except sqlite3.OperationalError:
            print('table people already exists')

    def get_all_data(self):
        cur = self.con.cursor()
        return cur.execute("SELECT * FROM people").fetchall()

    def _insert_fake_data(self):
        cur = self.con.cursor()
        cur.execute(
            """INSERT INTO people VALUES
                ('Profile1', 'profile1@gmail.com', 'Address1', 1, 'Sydney', 'New South Wales'),
                ('Profile2', 'profile2@gmail.com', 'Address2', 2, 'Melbourne', 'Victoria');"""
        )
        self.con.commit()

    def insert_person(self, name, email, street, number, city, state):
        cur = self.con.cursor()
        try:
            cur.execute(
                f"""INSERT INTO people VALUES
                    ('{name}', '{email}', '{street}', {number}, '{city}', '{state}');"""
            )
            self.con.commit()
            return 'success'
        except sqlite3.IntegrityError as e:
            print(e)
            return e

    def remove_person(self, email):
        cur = self.con.cursor()
        cur.execute(
            f"""DELETE FROM people WHERE email='{email}';"""
        )
        self.con.commit()

    def get_person(self, p_email: str):
        cur = self.con.cursor()
        return cur.execute(f'SELECT * FROM people WHERE email = "{p_email}"').fetchall()[0]


if __name__ == '__main__':
    with DB() as db:
        db.create_table_people()

    with DB() as db:
        res_all = db.get_all_data()
        print(res_all)

    with DB() as db:
        res_single = db.get_person('profile2@gmail.com')
        print(res_single)

