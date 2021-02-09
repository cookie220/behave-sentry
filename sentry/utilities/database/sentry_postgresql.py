import psycopg2
from psycopg2.extras import RealDictCursor


class PostgreSQL:
    def __init__(self, postgresql_hostname, postgresql_database, postgresql_username, postgresql_password):
        self.postgresql_database = postgresql_database
        self.postgresql_username = postgresql_username
        self.postgresql_password = postgresql_password
        self.postgresql_hostname = postgresql_hostname

        self.conn = self.get_connect()
        if self.conn:
            self.cur = self.conn.cursor()

    # get connection object
    def get_connect(self):
        conn = False
        try:
            conn = psycopg2.connect(
                database=self.postgresql_database,
                user=self.postgresql_username,
                password=self.postgresql_password,
                host=self.postgresql_hostname,
                cursor_factory=RealDictCursor
            )
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        return conn

    # execute query sql
    def exec_query(self, sql):
        res = ""
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
        except (Exception, psycopg2.OperationalError) as error:
            print('Error while query sql', error)
        finally:
            # closing database connection.
            if self.conn:
                self.cur.close()
                self.conn.close()
                print("PostgreSQL connection is closed")
        return res

    # execute update/insert/delete sql
    def exec_non_query(self, sql):
        flag = False
        try:
            self.cur.execute(sql)
            self.conn.commit()
            flag = True
        except (Exception, psycopg2.OperationalError) as error:
            flag = False
            self.conn.rollback()
            print('Error while update/insert/delete sql', error)
        finally:
            # closing database connection.
            if self.conn:
                self.cur.close()
                self.conn.close()
                print("PostgreSQL connection is closed")
        return flag



