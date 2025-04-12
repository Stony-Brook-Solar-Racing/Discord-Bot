import psycopg
from datetime import datetime
from datetime import timedelta

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
    def shop_closed(self):
        with self.connection.cursor() as cur:
            # Get whos in shop
            members = self.people_in()
            for person in members:
                # Get time delta
                cur.execute("""
                            SELECT last_swipe, shop_time
                            FROM members
                            WHERE first_name = %s AND last_name = %s
                            """,
                            (person[0], person[1]))
                time = cur.fetchone()
                time_delta = datetime.now() - time[0]
                total_time = time[1] + time_delta if time_delta < timedelta(hours=1) else time[1] + timedelta(hours=1) 

                # Sign the person out and update their time
                cur.execute("""
                            UPDATE members
                            SET in_shop = False, shop_time = %s
                            WHERE first_name = %s AND last_name = %s
                            """,
                            (total_time, person[0], person[1]))
                cur.execute("""
                            INSERT INTO logs
                            VALUES (%s, %s, False, NOW())
                            """,
                            (person[0], person[1]))

            self.connection.commit()
    
    # add a sign in entry to the main table
    def add_person(self, first_name, last_name) -> bool():
        with self.connection.cursor() as cur:
            first_name = first_name.lower()
            last_name = last_name.lower()

            # Check if the person is already in
            exists_or_in = self.person_in(first_name, last_name)
            if exists_or_in == True: return False

            # Change in_shop or add person to members table
            if exists_or_in == None:
                # shop time 1 for now
                cur.execute("""
                            INSERT INTO members
                            VALUES (%s, %s, True, NOW())
                            """,
                            (first_name, last_name))
            else:
                cur.execute("""
                            UPDATE members
                            SET in_shop = True, last_swipe = NOW()
                            WHERE first_name = %s AND last_name = %s
                            """,
                            (first_name, last_name))
            self.connection.commit();

            # Insert person into logs table
            cur.execute("""
                   INSERT INTO logs
                   VALUES (%s, %s, True, NOW())
                 """,
                        (first_name, last_name))
            self.connection.commit();
        return True

    def remove_person(self, first_name, last_name) -> bool():
        # add a sign out entry to the main table
        # also remove them from the other table
        with self.connection.cursor() as cur:
            first_name = first_name.lower()
            last_name = last_name.lower()

            # Check if person is in or even exists
            exists_or_in = self.person_in(first_name, last_name)
            if exists_or_in == False or exists_or_in == None: return False

            # Get the time delta
            cur.execute("""
                    SELECT last_swipe, shop_time
                    FROM members
                    WHERE first_name = %s AND last_name = %s
                    """,
                        (first_name, last_name))
            time = cur.fetchone()
            time_delta = datetime.now() - time[0]
            total_time = time[1] + time_delta
            
            # Sign out the person if they are in and exist
            cur.execute("""
                        UPDATE members
                        SET in_shop = False, shop_time = %s
                        WHERE first_name = %s AND last_name = %s
                        """,
                        (total_time, first_name, last_name))
            cur.execute("""
                        INSERT INTO logs
                        VALUES (%s, %s, False, NOW())
                        """,
                        (first_name, last_name))
            self.connection.commit()
        return True


    def ryan(self):
        if(self.person_in("ryan2", "tang")):
            self.remove_person("ryan2", "tang")
        else:
            self.add_person("ryan2", "tang")

if __name__ == "__main__":
    print("In freakydb, TESTING")
    db = solardb()
    print(db.people_in())
