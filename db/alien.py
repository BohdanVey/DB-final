import psycopg2
import os
import time
import datetime

try:
    from db import DBConnect
    from person import Person
    from ship import Ship
except:
    from .db import DBConnect
    from .person import Person
    from .ship import Ship


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

    def check_alive(self, alien_id):
        self.cur.execute(f"SELECT * FROM kills WHERE alien_id={alien_id}")
        return len(self.cur.fetchall()) == 0

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
        ship_from, _, time2 = Person().get_ship_specific_time(person_id, time1)
        print(time1, time2)
        Ship().update_ship(ship_from, person_id, time1, time2)
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

    def get_stolen(self, alien_id, N, start_time, finish_time):
        self.cur.execute(f"""
        WITH constants (F_start, T_end, N_amount, A_alien_id) AS (
	VALUES ('{start_time}', '{finish_time}', {N}, {alien_id})
)
SELECT person_id FROM Stolen, constants
WHERE alien_id = A_alien_id
AND time >= TO_DATE(F_start, 'YYYY-MM-DD')
AND time <= TO_DATE(T_end, 'YYYY-MM-DD')
GROUP BY person_id, N_amount
HAVING COUNT(person_id) >= N_amount;
""")

        ids = [x[0] for x in self.cur.fetchall()]
        if not ids:
            return []
        ids = str(tuple(ids))
        if ids[-2] == ',':
            ids = ids[:-2] + ')'
        self.cur.execute(f"SELECT * FROM person WHERE person_id in {ids}")
        return self.cur.fetchall()

    def get_excursion(self, alien_id, N):
        self.cur.execute(f"""SELECT ep.excursion_id FROM excursion e INNER JOIN excursionPerson ep 
ON ep.excursion_id = e.excursion_id
WHERE alien_id = {alien_id}
GROUP BY ep.excursion_id
HAVING COUNT(person_id) >= {N};
""")
        ids = [[x[0]] for x in self.cur.fetchall()]
        return ids

    def get_stillN(self, start_time, finish_time, N):
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        finish_time = datetime.datetime.strptime(finish_time, "%Y-%m-%d")
        self.cur.execute(f""" SELECT s.alien_id FROM alien a 
        INNER JOIN stolen s ON a.alien_id = s.alien_id 
        WHERE time >= '{start_time}' AND time <= '{finish_time}'
        GROUP BY s.alien_id HAVING COUNT(DISTINCT person_id) >= {N};
""")
        ids = [x[0] for x in self.cur.fetchall()]
        if not ids:
            return []
        ids = str(tuple(ids))
        if ids[-2] == ',':
            ids = ids[:-2] + ')'
        self.cur.execute(f"SELECT * FROM alien WHERE alien_id in {ids}")
        return self.cur.fetchall()

    def get_ships(self, alien_id, start_time, finish_time):
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        finish_time = datetime.datetime.strptime(finish_time, "%Y-%m-%d")

        self.cur.execute(f"""
        SELECT s.ship_id,s.ship_name FROM ship s INNER JOIN experiment e ON s.ship_id = e.ship_id 
        INNER JOIN experimentAlien ea ON ea.experiment_id = e.experiment_id 
        WHERE ea.alien_id = {alien_id} AND time >= '{start_time}' AND time <= '{finish_time}' GROUP BY s.ship_id ORDER BY COUNT(*) DESC;
""")
        return self.cur.fetchall()