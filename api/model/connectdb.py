import psycopg2
import psycopg2.extras
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse


def Connection():
    results = urlparse("postgresql+psycopg2://postgres:@localhost:5432")
    user = results.username
    password = results.password
    host = results.hostname
    dbname = results.path[1:]
    conn = psycopg2.connect(dbname='demo', user='postgres', host='localhost', password='@bashtech1234')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTs mt_requests (request_id serial PRIMARY KEY, requestname varchar, description varchar);")
    cursor.execute("CREATE TABLE IF NOT EXISTs mt_users (user_id serial PRIMARY KEY, username varchar, email varchar, password varchar);")
    conn.commit()

    return conn
