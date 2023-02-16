""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import os

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    pool = ThreadedConnectionPool(1, 10, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def add_response (name, dateAgain, futureDate, additionalFeedback):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO responses (name, dateAgain, futureDate, additionalFeedback) values (%s, %s, %s, %s);", (name, dateAgain, futureDate, additionalFeedback))

def get_responses(reverse):
	query = "SELECT * from responses ORDER BY id;" if not reverse else "SELECT * from responses ORDER BY id DESC;"
	with get_db_cursor(True) as cur:
		cur.execute(query)
		return cur.fetchall()