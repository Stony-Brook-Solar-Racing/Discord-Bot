import psycopg
from datetime import datetime

import json
with open('/home/racer/solardb_config.json', 'r') as conf:
    config = json.load(conf)

DBNAME = "db"

class solardb:
    def __init__(self):
        self.connection = psycopg.connect(f"dbname={config['dbname']} user={config['user']}")

    # return whether the person is in the shop
    def person_in(self, first_name, last_name) -> bool():
        first_name = first_name.lower()
        last_name = last_name.lower()
        with self.connection.cursor() as cur:
            cur.execute("""
                SELECT in_shop
                FROM members
                WHERE first_name = %s AND last_name = %s
                """,
                        (first_name, last_name))
            data = cur.fetchone()
            return None if data == None else data[0];
    
    def people_in(self) -> list[list[str]]:
        with self.connection.cursor() as cur:
            cur.execute("""
                        SELECT first_name, last_name
                        FROM members
                        WHERE in_shop = True
                        """)
            return cur.fetchall()

    def sign_everyone_out(self):
        # sign everyone out
        # find people currently in the shop, then write sign out entries for them 
        with self.connection.cursor() as cur:
            # Gets whos in the shop
            members = self.people_in()

            # Signout everyone who is in
            cur.execute("""
                        UPDATE members
                        SET in_shop = False
                        WHERE in_shop = True
                        """)
            for member in members:
                cur.execute("""
                            INSERT INTO logs
                            VALUES (%s, %s, False, NOW())
                            """,
                            (member[0], member[1]))
            self.connection.commit()
        return True

    def get_leaderboard(self):
        with self.connection.cursor() as cur:
            cur.execute("""
                        SELECT first_name,last_name,shop_time
                        FROM members
                        ORDER BY shop_time DESC
                        """)
            people = cur.fetchall()
            return people

if __name__ == "__main__":
    print("In freakydb, TESTING")
    db = solardb()
    print(db.get_leaderboard()[0][2])
