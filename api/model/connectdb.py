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
    conn = psycopg2.connect(dbname='maintenancetracker', user='postgres', host='localhost', password='@bashtech1234')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    """Create users table """

    cursor.execute("""CREATE TABLE IF NOT EXISTs mt_users 
    (user_id serial PRIMARY KEY, 
    username varchar, 
    email varchar,
    password varchar);""")


    """ Create requests table """

    cursor.execute("""CREATE TABLE IF NOT EXISTs mt_requests (request_id serial PRIMARY KEY, 
    requestname varchar, 
    description varchar, 
    status varchar, 
    owner int, 
    date_created TIMESTAMP, 
    date_modified TIMESTAMP, 
    FOREIGN KEY (owner) REFERENCES mt_users(user_id));""")

    """ Create blacklist table """

    cursor.execute("CREATE TABLE IF NOT EXISTs blacklist_tokens \
    (id serial PRIMARY KEY, \
    jti varchar);")

    """ Create test_db tables """

    cursor.execute("CREATE TABLE IF NOT EXISTs test_db \
    (user_id serial PRIMARY KEY, \
    username varchar, \
    email varchar, \
    password varchar);")
    conn.commit()

    return conn

def rollback(cls):
    """Delete all data from the tables"""

    con = Connection()
    cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("DELETE FROM {}".format(cls.__tablename__))
    con.commit()
    