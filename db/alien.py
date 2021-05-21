import psycopg2
import os
import time
import datetime

try:
    from db import DBConnect
    from person import Person
except:
    from .db import DBConnect
    from .person import Person


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

    def still_person(self, alien_id, person_id, ship_id, time1):
        _, time2 = Person().get_nearest_ship(person_id, time1)
        self.cur.execute(
            f"INSERT INTO Stolen (person_id, alien_id, ship_id, time) VALUES ({person_id},{alien_id},{ship_id},'{time1}')")
        if not time2:
            time2 = "9999-12-31"
            time2 = datetime.datetime.strptime(time2, "%Y-%m-%d")
        time1 = datetime.datetime.strptime(time1, "%Y-%m-%d")
        print(time2)
        self.cur.execute(
            f"INSERT INTO personShip (person_id, ship_id, start_time, finish_time) VALUES ({person_id},{ship_id},'{time1}','{time2}')")
        self.con.commit()

    def transfer_person(self, alien_id, person_id, ship_id, time1):
        ship_from, time2 = Person().get_nearest_ship(person_id, time1)
        self.cur.execute(
            f"UPDATE personShip SET finish_time='{time1}' WHERE ship_id = {ship_from} and finish_time='{time2}'")
        self.cur.execute(
            f"INSERT INTO personShip (person_id, ship_id, start_time, finish_time) VALUES ({person_id},{ship_id},'{time1}','{time2}')")
        self.cur.execute(
            f"INSERT INTO transfer (person_id,alien_id,ship_from_id,ship_to_id,time) VALUES ({person_id},{alien_id},{ship_from},{ship_id},'{time1}')"
        )
        self.con.commit()

    def make_excursion(self, alien_id, people_id, time):
        time = datetime.datetime.strptime(time, "%Y-%m-%d")
        self.cur.execute(f"INSERT INTO excursion (alien_id,time) VALUES ({alien_id},'{time}') RETURNING excursion_id")
        id = self.cur.fetchone()[0]
        txt = ''.join([f"({id},{x})," for x in people_id])[:-1]
        self.cur.execute(
            f"INSERT INTO excursionPerson (excursion_id,person_id) VALUES {txt}")
        self.con.commit()


if __name__ == '__main__':
    Alien().make_excursion(14, [1, 2, 3], '2000-12-12')
