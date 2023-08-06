from configparser import ConfigParser
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
import sys



class DatabaseHandler(object):

    def __init__(self, config_file, config_file_section):
        self.config_file = config_file
        self.config_file_section = config_file_section
        self.conn = None 

    
    def read_db_config(self):
        
        # create a parser
        parser = ConfigParser()

        #read config file
        parser.read(self.config_file)

        #get postgresql section
        db = {}
        if parser.has_section(self.config_file_section):
            params = parser.items(self.config_file_section)

            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in file {1}'.format(self.config_file_section, self.config_file))
        
        return db
    
    def connect(self):

        try:
            # read connection parameters
            params = self.read_db_config()

            self.conn = psycopg2.connect(**params)

        except Exception as ex:
            if str(ex)[:6] == 'FATAL:':
                sys.exit("Database connection error: %s" % str(ex)[8:])
            else:
                raise ex

    def get_cursor(self):
        """Create a cursor
        :return: cursor
        """
        if self.conn is None or self.conn.closed:
            self.connect()
        curs = self.conn.cursor(cursor_factory=DictCursor)
        
        return curs

    def close(self):
        """Close the database connection"""
        if self.conn and not self.conn.closed:
            self.conn.close()
        self.conn = None

    def commit(self):
        """Commit currently open transaction"""
        self.conn.commit()

    def rollback(self):
        """Roll back currently open transaction"""
        self.conn.rollback()

    def execute(self, query, args=None):
        """Create a cursor, execute a query and return the cursor
        :param query: text of the statement to execute
        :param args: arguments to query
        :return: cursor
        """
        if self.conn is None or self.conn.closed:
            self.connect()
        curs = self.conn.cursor(cursor_factory=DictCursor)
        try:
            curs.execute(query, args)
        except Exception as exc:
            self.conn.rollback()
            curs.close()
            raise exc
        return curs

    def fetchone(self, query, args=None):
        """Execute a single row SELECT query and return row
        :param query: a SELECT query to be executed
        :param args: arguments to query
        :return: a psycopg2 DictRow
        The cursor is closed.
        """
        curs = self.execute(query, args)
        row = curs.fetchone()
        curs.close()
        return row

    def fetchall(self, query, args=None):
        """Execute a SELECT query and return rows
        :param query: a SELECT query to be executed
        :param args: arguments to query
        :return: a list of psycopg2 DictRow's
        The cursor is closed.
        """
        curs = self.execute(query, args)
        rows = curs.fetchall()
        curs.close()
        return rows

    def copy_to(self, path, table, sep=','):
        """Execute a COPY command to a file
        :param path: file name/path to copy into
        :param table: possibly schema qualified table name
        :param sep: separator between columns
        """
        if self.conn is None or self.conn.closed:
            self.connect()
        with open(path, 'w') as f:
            curs = self.conn.cursor()
            try:
                curs.copy_to(f, table, sep)
            except:
                curs.close()
                raise

    def sql_copy_to(self, sql, path):
        """Execute an SQL COPY command to a file
        :param sql: SQL copy command
        :param path: file name/path to copy into
        """
        if self.conn is None or self.conn.closed:
            self.connect()
        with open(path, 'w') as f:
            curs = self.conn.cursor()
            try:
                curs.copy_expert(sql, f)
            except:
                curs.close()
                raise
    
    def sql_copy_from(self, sql, path):
        """Execute an SQL COPY command from a file
        :param sql: SQL copy command
        :param path: file name/path to copy from
        """
        if self.conn is None or self.conn.closed:
            self.connect()
        with open(path, 'r') as f:
            curs = self.conn.cursor()
            try:
                curs.copy_expert(sql, f)
            except:
                curs.close()
                raise

    def copy_from(self, path, table, sep=','):
        """Execute a COPY command from a file
        :param path: file name/path to copy from
        :param table: possibly schema qualified table name
        :param sep: separator between columns
        """
        if self.conn is None or self.conn.closed:
            self.connect()
        with open(path, 'r') as f:
            curs = self.conn.cursor()
            try:
                curs.copy_from(f, table, sep)
            except:
                curs.close()
                raise