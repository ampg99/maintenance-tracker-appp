from psycopg2.extensions import adapt, register_adapter, AsIs
from flask import jsonify
import json
import psycopg2.extras
from datetime   import datetime
from .connectdb import Connection, rollback

conn = Connection()

APPROVED = "Approved"
REJECTED = "Rejected"
RESOLVED = "Resolved"
NEW = "New"

class RequestsModel:
    __tablename__ = "mt_requests"
    def __init__(self, owner=None, date_created=datetime.now(), date_modified=datetime.now(), \
    requestname="", description="", status=""):
       super().__init__()
       self.requestname = requestname
       self.description = description
       self.owner = owner
       self.status = NEW
       self.date_modified = date_modified
       self.date_created = date_created
       rollback(RequestsModel)

    def json(self):
        """
        convert RequestsModel object into json
        """
        return {
            'requestname': self.requestname, 
            'description': self.description,
            'status': self.status,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }

    def find_all(self):
        """Gets all the requests from the database"""
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'SELECT * FROM mt_requests'
        ex_query = cursor.execute(query)
        data = cursor.fetchall()

        return data

    @classmethod
    def find_by_name(cls, requestname):
        """
        objective: finds an item in the database by name
        :param name: str - item name
        :return: json - row data in object form, None otherwise
        """
        cursor = conn.cursor()

        query = 'SELECT * FROM mt_requests WHERE requestname=?'
        result = cursor.execute(query, (requestname,))
        row = result.fetchone()
        try:
            return cls(*row) if row else None
        except Exception as e:
            print(e)

    def find_by_field(self, field, value):
        if self.find_all() is None:
            return {}
        for item in self.find_all():
            if item[field] == value:
                return item

    @classmethod
    def find_by_id(cls, _request_id):
        """
        objective: searches the database by request id
        :param _id: int - unique user identifier
        :return: New User object if exists, otherwise None
        """
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = 'SELECT * FROM mt_requests WHERE request_id=%s'
        ex_query = cursor.execute(query, (_request_id,))
        row = cursor.fetchone()
        if not row:
            return None
        else:
            return {
                'request_id': row['request_id'],
                'requestname': row['requestname'],
                'description': row['description'],
                'status': row['status'],
                'owner': row['owner'],
                'date_created': row['date_created'],
                'date_modified': row['date_modified']
            }

    def insert(self, my_request):
        """
        objective: inserts object to database
        :return: None
        """
        cursor = conn.cursor()

        query = "INSERT INTO mt_requests (requestname, \
        description, status, owner, date_created, date_modified) \
        values (%s, %s, %s, %s, %s, %s) RETURNING request_id"
        cursor.execute(query, (
            self.requestname,
            self.description,
            self.status,
            self.owner,
            self.date_created,
            self.date_modified
        ))

        conn.commit()

    def update(self):
        """
        objective: modify the contents of item in database.
        :return: None
        """
        cursor = conn.cursor()

        query = "UPDATE mt_requests SET description=%s, \
        requestname=%s, , status=%s, \
        owner=%s, date_modified=%s \
        WHERE request_id=%s"
        cursor.execute(query, (self.description, self.requestname, \
        self.status, self.owner, self.date_modified))

        conn.commit()

