import psycopg2
import os
import time
import datetime

try:
    from db import DBConnect
    from ship import Ship
except:
    from .db import DBConnect
    from .ship import Ship


class Person(DBConnect):
    def __init__(self):
        super(Person, self).__init__()

    def get_all(self, params=['*']):
        self.cur.execute(f"SELECT {','.join(params)} FROM person")
        return self.cur.fetchall()

    def get_ship_specific_time(self, _id, time):
        self.cur.execute(
            f"SELECT ship_id,start_time,finish_time FROM personShip WHERE person_id = {_id} AND start_time < '{time}' AND '{time}' < finish_time")
        try:
            return self.cur.fetchall()[0]
        except IndexError:
            return -1, None, None

    def get_nearest_ship(self, _id, time):
        time = datetime.datetime.strptime(time, "%Y-%m-%d")

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

    def escape_from(self, person_id, time1):
        ship_from, _, time2 = self.get_ship_specific_time(person_id, time1)
        print(ship_from, time2, time1)
        Ship().update_ship(ship_from, person_id, time1, time2)

    def make_experiment(self, person_id, aliens_id, time):
        time = datetime.datetime.strptime(time, "%Y-%m-%d")
        ship_id, _, _ = self.get_ship_specific_time(person_id, time)
        self.cur.execute(
            f"INSERT INTO experiment (person_id,ship_id,time) VALUES ({person_id},{ship_id},'{time}') RETURNING experiment_id")
        id = self.cur.fetchone()[0]
        txt = ''.join([f"({id},{x})," for x in aliens_id])[:-1]
        self.cur.execute(
            f"INSERT INTO experimentAlien (experiment_id,alien_id) VALUES {txt}")
        self.con.commit()

    def kill_alien(self, person_id, alien_id, time):
        time = datetime.datetime.strptime(time, "%Y-%m-%d")
        ship_id, _, _ = self.get_ship_specific_time(person_id, time)
        self.cur.execute(
            f"INSERT INTO kills (person_id,alien_id,time) VALUES ({person_id},{alien_id},'{time}')")
        self.con.commit()

    def get_visited(self, person_id, start_time, finish_time):
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        finish_time = datetime.datetime.strptime(finish_time, "%Y-%m-%d")
        self.cur.execute(
            f"SELECT DISTINCT s.ship_id,s.ship_name FROM ship s INNER JOIN personShip ps ON ps.ship_id = s.ship_id WHERE ps.person_id = {person_id} AND ps.start_time < '{finish_time}' AND"
            f" ps.finish_time > '{start_time}' GROUP BY s.ship_id")
        return self.cur.fetchall()

    def get_stolen(self, person_id, N, start_time, finish_time):
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        finish_time = datetime.datetime.strptime(finish_time, "%Y-%m-%d")
        self.cur.execute(f"""
SELECT alien_id FROM Stolen
WHERE person_id = {person_id}
AND time >= '{start_time}'
AND time <= '{finish_time}'
GROUP BY alien_id, {N}
HAVING COUNT(alien_id) >= {N};
""")
        ids = [x[0] for x in self.cur.fetchall()]
        if not ids:
            return []
        ids = str(tuple(ids))
        self.cur.execute(f"SELECT * FROM alien WHERE alien_id in {ids[:-2]})")
        return self.cur.fetchall()


if __name__ == '__main__':
    import datetime

    print(Person().get_nearest_ship(1, '0050-12-12'))
