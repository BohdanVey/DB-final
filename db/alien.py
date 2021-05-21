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

    def check_alien(self, name, surname):
        self.cur.execute(f"SELECT * FROM alien WHERE name='{name}' AND surname='{surname}'")
        return len(list(self.cur.fetchall())) > 0

    def add_alien(self, name, surname, url=None):
        if url:
            self.cur.execute(f"INSERT INTO alien (name,surname,url) VALUES ('{name}','{surname}','{url}')")
        else:
            self.cur.execute(f"INSERT INTO alien (name,surname) VALUES ('{name}','{surname}')")

        self.con.commit()

    def still_person(self, alien_id, person_id, ship_id, time):
        self.cur.execute(
            f"INSERT INTO Stolen (person_id, alien_id, ship_id, time) VALUES ({person_id},{alien_id},{ship_id},'{time}')")
        self.con.commit()
