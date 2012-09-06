import urlparse
from migranto.lib.error import APIError
from migranto.lib.printer import Printer

class Db:

    schemes = ('pgsql', 'sqlite')

    def __init__(self, db_url, out = False):
        self.options = self.parseDBString(db_url)
        self.out = out

        try:
            if self.options.scheme == 'pgsql':
                import psycopg2
                import psycopg2.extensions
                psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
                psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
                self.dbname = self.options.path[1:]
                self.conn = psycopg2.connect(database=self.dbname, user=self.options.username, password=self.options.password, host=self.options.hostname, port=self.options.port)

            elif self.options.scheme == 'sqlite':
                import sqlite3
                self.dbname = self.options.path
                self.conn = sqlite3.connect(self.dbname)

        except Exception, exc:
            raise APIError(exc)

        self.c = self.conn.cursor()

    @property
    def scheme(self):
        return self.options.scheme

    def parseDBString(self, db_string):
        r = urlparse.urlparse(db_string)

        if r.scheme in self.schemes:
            return r
        else:
            raise APIError('Provide a correct database connection string')

    def printData(self, out):
        printer = Printer(out, [20, 10, 20])
        printer.printRow(('Name', 'Migration', 'Date'))

        for row in self.c:
            printer.printRow(row)

    def fetchOneResult(self, sql, data):
        try:
            self.c.execute(sql, data)
        except Exception:
            return None

        r = self.c.fetchone()

        if r:
            return r[0]
        else:
            return None

    def executeFile(self, filename):
        if filename:
            sql = open(filename, 'r').read()

            if sql.strip():
                if self.out:
                    print >> self.out, sql
                else:
                    if self.scheme == 'sqlite':
                        self.c.executescript(sql)

                    elif self.scheme == 'pgsql':
                        self.c.execute(sql)


    def execute(self, sql, data = None):

        if self.out:
            print >> self.out, sql % data
        else:
            if data:
                self.c.execute(sql, data)
            else:
                self.c.execute(sql)

    def begin(self):
        if self.out:
            print >> self.out, 'BEGIN;'
        else:
            self.c.execute('BEGIN')

    def commit(self):
        if self.out:
            print >> self.out, 'COMMIT;'
        else:
            self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.c.close()
        self.conn.close()