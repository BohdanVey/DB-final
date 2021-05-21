import psycopg2
import os
import time
from .db import DBConnect


class Person(DBConnect):
    def __init__(self):
        super(Person, self).__init__()

    def get_all(self, params=['*']):
        self.cur.execute(f"SELECT {','.join(params)} FROM person")
        return self.cur.fetchall()

    def get_by_id(self, _id, params=['*']):
        self.cur.execute(f"SELECT {','.join(params)} FROM person WHERE person_id={_id}")
        return self.cur.fetchall()[0]

    def check_person(self, name, surname):
        self.cur.execute(f"SELECT * FROM person WHERE name='{name}' AND surname='{surname}'")
        return len(list(self.cur.fetchall())) > 0

    def add_person(self, name, surname, url=None):
        if url:
            self.cur.execute(f"INSERT INTO person (name,surname,url) VALUES ('{name}','{surname}','{url}')")
        else:
            self.cur.execute(f"INSERT INTO person (name,surname) VALUES ('{name}','{surname}')")

        self.con.commit()
