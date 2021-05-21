import psycopg2
import os
import time
from .db import DBConnect


class Ship(DBConnect):
    def __init__(self):
        super(Ship, self).__init__()

    def get_all(self, params=['*']):
        self.cur.execute(f"SELECT {','.join(params)} FROM ship")
        return self.cur.fetchall()

    def get_by_id(self, _id, params=['*']):
        self.cur.execute(f"SELECT {','.join(params)} FROM ship WHERE ship_id={_id}")
        return self.cur.fetchall()[0]

    def check_ship(self, name, surname=''):
        self.cur.execute(f"SELECT * FROM ship WHERE ship_name='{name}'")
        return len(list(self.cur.fetchall())) > 0

    def add_ship(self, name, surname=None, url=None):
        self.cur.execute(f"INSERT INTO ship (ship_name) VALUES ('{name}')")
        self.con.commit()
