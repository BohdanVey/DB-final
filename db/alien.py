import psycopg2
import os
import time
from .db import DBConnect


class Alien(DBConnect):
    def __init__(self):
        super(Alien, self).__init__()

    def get_all(self, params=['*']):
        self.cur.execute(f"SELECT {','.join(params)} FROM alien")
        return self.cur.fetchall()

    def get_by_id(self, _id, params=['*']):
        self.cur.execute(f"SELECT {','.join(params)} FROM alien WHERE alien_id={_id}")
        return self.cur.fetchall()[0]
