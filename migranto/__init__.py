#!/usr/bin/python
import argparse
import sys
from lib.main import Migranto

def main():

    parser = argparse.ArgumentParser(description='Simple SQL migration tool')

    parser.add_argument('--database', '-d', dest='database', metavar='URL', required=True,
                        help='database url (pgsql://user:password@host:port/dbname or sqlite://path/to/data.base)')

    parser.add_argument('--name', '-n', dest='name',
                        help='migration set name')

    parser.add_argument('--path', '-p', dest='path',
                        help='path to migrations dir')

    parser.add_argument('--migration', '-m', dest='migration', type=int, metavar = 'N',
                        help='migration step (last migration if omitted, 0 - before first migration)')

    parser.add_argument('--verbose', '-v', dest='verbose', action='count', default=False,
                        help='verbose mode')

    parser.add_argument('--storage', '-s', dest='storage', metavar='NAME', default='migranto',
                        help='migranto table name for data (default is migranto)')

    parser.add_argument('--fake', '-f', dest='fake', action='count', default=False,
                        help='fake migration (no sql applied to database, except migration number)')

    migranto = Migranto(parser.parse_args())

    try:
        migranto.run()
    except Exception, exc:
        print exc
        sys.exit(0)