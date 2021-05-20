import psycopg2
import os
import time


class DBConnect:
    P = None

    def __init__(self):
        if self.P is None:
            while True:
                try:
                    self.con = psycopg2.connect(
                        host=os.getenv("DB_HOST"),
                        database=os.getenv("DB_DATABASE"),
                        user=os.getenv("DB_USER"),
                        password=os.getenv('DB_PASSWORD')
                    )
                    self.cur = self.con.cursor()
                    break
                except NameError as e:
                    time.sleep(5)
                    continue
            DBConnect.P = self
        else:
            self.con = self.P.con
            self.cur = self.P.cur




