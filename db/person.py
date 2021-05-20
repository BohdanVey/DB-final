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
