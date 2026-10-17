import pymysql
from pymysql import cursors
from Config.db_config import DB_CONFIG

class DBUtil:
    @staticmethod
    def open_db():
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            db=DB_CONFIG["db"],
            charset="utf8",
            cursorclass=cursors.DictCursor
        )
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def read_one(sql, cursor):
        cursor.execute(sql)
        return cursor.fetchone()

    @staticmethod
    def write_db(sql, cursor):
        result = cursor.execute(sql)
        return result > 0

    @staticmethod
    def release(conn, cursor):
        if cursor: cursor.close()
        if conn: conn.close()