import json
from datetime import datetime, timedelta

import psycopg

with open("config.json", "r") as conf:
    config = json.load(conf)


class solardb:
    def __init__(self):
        self.connection = psycopg.connect(
            f"dbname={config['psql_db']} user={config['psql_user']}"
        )

    def next_session(self):
        with self.connection.cursor() as cur:
            cur.execute("SELECT nextval('session_seq')")
            return cur.fetchone()[0]

    # return whether the person is in the shop
    def person_in(self, first_name, last_name) -> bool():
        first_name = first_name.lower()
        last_name = last_name.lower()
        with self.connection.cursor() as cur:
            cur.execute(
                """
                SELECT in_shop
                FROM members
                WHERE first_name = %s AND last_name = %s
                """,
                (first_name, last_name),
            )
            data = cur.fetchone()
            return None if data is None else data[0]

    def people_in(self) -> list[list[str]]:
        with self.connection.cursor() as cur:
            cur.execute(
                """
                        SELECT id_hash, first_name, last_name
                        FROM members
                        WHERE in_shop = True
                        """
            )
            return cur.fetchall()

    def people_in_names(self) -> list[list[str]]:
        with self.connection.cursor() as cur:
            cur.execute(
                """
                        SELECT first_name, last_name
                        FROM members
                        WHERE in_shop = True
                        """
            )
            return cur.fetchall()

    def sign_everyone_out(self):
        # sign everyone out
        # find people currently in the shop, then write sign out entries for them
        with self.connection.cursor() as cur:
            # Gets whos in the shop
            members = self.people_in()

            # Signout everyone who is in
            cur.execute(
                """
                        UPDATE members
                        SET in_shop = False
                        WHERE in_shop = True
                        """
            )
            for member in members:
                cur.execute(
                    """
                            INSERT INTO logs
                            VALUES (%s, %s, %s, False, NOW())
                            """,
                    (member[0], member[1]),
                    member[2],
                )
            self.connection.commit()
        return True

    def import_tasks(self, tasks):
        query = "INSERT INTO tasks (category, task) VALUES (%s, %s);"
        with self.connection.cursor() as cur:
            try:
                cur.executemany(query, tasks)
                self.connection.commit()
            except Exception as _:
                self.connection.rollback()

    def get_tasks(self, filter=None):
        if filter is None:
            query = "SELECT id, category, task, complete FROM tasks ORDER BY id ASC;"
            params = None
        else:
            query = "SELECT id, category, task, complete FROM tasks WHERE category ILIKE %s ORDER BY id ASC;"
            params = (f"%{filter}%",)

        with self.connection.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        return rows

    def purge_tasks(self):
        query = "DELETE FROM tasks WHERE complete = True;"
        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()

    def complete_tasks(self, id_list):
        query = """
            UPDATE tasks 
            SET complete = True 
            WHERE id = ANY(%s) 
            RETURNING id, task;
        """

        with self.connection.cursor() as cur:
            cur.execute(query, (id_list,))
            updated_rows = cur.fetchall()
            self.connection.commit()

        return updated_rows

    def get_leaderboard(self):
        with self.connection.cursor() as cur:
            cur.execute(
                """
                        SELECT first_name, last_name, shop_time
                        FROM members
                        ORDER BY shop_time DESC
                        """
            )
            people = cur.fetchall()
            return people

    def shop_closed(self):
        with self.connection.cursor() as cur:
            # Get whos in shop
            members = self.people_in()
            for person in members:
                id_hash = person[0]
                # Get time delta
                cur.execute(
                    """
                            SELECT last_swipe, shop_time
                            FROM members
                            WHERE id_hash = %s
                            """,
                    (id_hash,),
                )
                time = cur.fetchone()
                time_delta = datetime.now() - time[0]
                total_time = (
                    time[1] + time_delta
                    if time_delta < timedelta(hours=1)
                    else time[1] + timedelta(hours=1)
                )

                # Sign the person out and update their time
                cur.execute(
                    """
                            UPDATE members
                            SET in_shop = False, shop_time = %s
                            WHERE id_hash = %s
                            """,
                    (total_time, id_hash),
                )
                cur.execute(
                    """
                            INSERT INTO logs
                            VALUES (%s, %s, %s, False, NOW())
                            """,
                    (id_hash, person[1], person[2]),
                )

            self.connection.commit()

    def add_time(self, first_name, last_name, hour):
        first_name = first_name.lower()
        last_name = last_name.lower()
        with self.connection.cursor() as cur:
            cur.execute(
                """
                SELECT last_swipe, shop_time
                FROM members
                WHERE first_name = %s AND last_name = %s
                """,
                (first_name, last_name),
            )

            row = cur.fetchone()
            if row is None:
                return None
            total_time = row[1] + timedelta(hours=hour)
            cur.execute(
                """
                UPDATE members
                SET in_shop = False, shop_time = %s
                WHERE first_name = %s AND last_name = %s
                """,
                (total_time, first_name, last_name),
            )

            self.connection.commit()
        return 1
