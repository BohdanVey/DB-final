import psycopg2
import os
import time
import datetime
try:
    from db import DBConnect
except:
    from .db import DBConnect

class Person(DBConnect):
    def __init__(self):
        super(Person, self).__init__()

    def get_all(self, params=['*']):
        self.cur.execute(f"SELECT {','.join(params)} FROM person")
        return self.cur.fetchall()

    def get_ship_specific_time(self, _id, time):
        self.cur.execute(
            f"SELECT ship_id,finish_time FROM personShip WHERE person_id = {_id} AND start_time < '{time}' AND '{time}' < finish_time")
        try:
            return self.cur.fetchall()[0]
        except IndexError:
            return -1, None

    def get_nearest_ship(self, _id, time):
        time = datetime.datetime.strptime(time, "%Y-%m-%d")
        print(_id, type(time), time)

        self.cur.execute(
            f"SELECT ship_id,start_time FROM personShip WHERE person_id = {_id} AND start_time > '{time}' ORDER BY start_time ")

        try:
            return self.cur.fetchall()[0]
        except IndexError:
            return -1, None

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


if __name__ == '__main__':
    import datetime

    print(Person().get_nearest_ship(1, '0050-12-12'))
