import psycopg2
import os
import time
import json
import datetime


class Person:
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
            Person.P = self
        else:
            self.con = self.P.con
            self.cur = self.P.cur


if __name__ == '__main__':
    Person().save_results('3286437378061599', Person().get_attributes('3286437378061599'))
