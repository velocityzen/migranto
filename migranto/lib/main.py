import os
import re
from migranto.lib.db import Db
from migranto.lib.error import APIError
from migranto.lib.utils import getFileListByMask
from migranto.lib import sql as SQL

class Migranto:

    def __init__(self, options):
        self.path = options.path
        self.dbstring = options.database
        self.name = options.name
        self.toStep = options.migration if options.migration is not None else 'max'
        self.nowStep = None
        self.topStep = 0
        self.verbose = options.verbose
        self.migrations = {}
        self.storage = options.storage
        self.home_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), '..')

    def dbConnect(self):
        self.db = Db(self.dbstring)
        self.SQL = getattr(SQL, self.db.scheme)

    def dbClose(self):
        self.db.close()

    def getLastMigration(self):
        self.nowStep = self.db.fetchOneResult(self.SQL['selectLatestMigration'].format(tablename = self.storage) , (self.name,))
        return self.nowStep

    def createNewMigration(self, name):
        try:
            self.db.begin()
            self.db.execute(self.SQL['insertMigration'].format(tablename = self.storage), (name,))
            self.db.commit()
        except Exception:
            self.db.rollback()
            self.db.execute(self.SQL['createTable'].format(tablename = self.storage))
            self.db.execute(self.SQL['insertMigration'].format(tablename = self.storage), (name,))
            self.db.commit()

    def loadMigrations(self):
        migration_files = getFileListByMask(self.path, ['*.sql'])

        r = re.compile('.*(\d+)_.*?(_rollback)?\.sql$', re.IGNORECASE)

        if migration_files:
            for migration_file in migration_files:
                m = r.findall(migration_file)[0]

                if m:
                    m_step = int(m[0])

                    if m_step in self.migrations:
                        migration = self.migrations[m_step]
                    else:
                        self.migrations[m_step] = migration = {}

                    if m[1]:
                        if "down" not in migration:
                            migration["down"] = migration_file
                        else:
                            raise APIError("Migration duplicates at %d step", m_step)
                    else:
                        if "up" not in migration:
                            migration["up"] = migration_file
                        else:
                            raise APIError("Migration duplicates at %d step", m_step)

                    if m_step > self.topStep:
                        self.topStep = m_step
                else:
                    continue
        else:
            raise APIError('No migration files found')

        if self.toStep == 'max':
            self.toStep = self.topStep


    def applyMigrations(self):
        if self.toStep > self.topStep:
            raise APIError('Top migration is %d' % self.topStep)

        # db is up to date
        if self.toStep == self.nowStep:
            raise APIError("Database for %s is up to date. No migration applied" % self.name )

        # down
        if self.toStep < self.nowStep:
            for i in range(self.nowStep, self.toStep, -1):
                self.applyMigration(self.migrations[i], 'down', i)

            return  self.toStep
        # up
        elif self.toStep > self.nowStep:
            # no migrations applied yet
            if not self.nowStep:
                self.nowStep = 1

            for i in range(self.nowStep, self.toStep + 1):
                self.applyMigration(self.migrations[i], 'up', i)

            return  self.toStep

    def applyMigration(self, migration, flow, number):
        if self.verbose:
            print "%s %d: %s" % (self.name, number, migration[flow])

        try:
            self.db.begin()
            self.db.executeFile(migration[flow])
            self.db.execute(self.SQL['updateMigration'].format(tablename = self.storage), ( number - 1 if flow == 'down' else number, self.name))
            self.db.commit()

        except Exception, exc:
            try:
                self.db.rollback()
            except Exception, rollback_exc:
                raise APIError('Error: ' + str(exc) + 'Rollback error: ' + str(rollback_exc))
            raise APIError('Error: ' + str(exc))

    def run(self):
        if self.verbose:
            print "Opening database connection"
        self.dbConnect()

        if self.verbose:
            print "Database: " + self.db.dbname

        self.loadMigrations()

        if self.getLastMigration() is None:
            self.createNewMigration(self.name)
            self.nowStep = 0

        if self.verbose:
            print "Migration for %s. Now %d / To %d / Max %d" % (self.name, self.nowStep, self.toStep, self.topStep)

        self.nowStep = self.applyMigrations()

        if self.verbose:
            print "Migration for %s complete with migration %d" % (self.name, self.nowStep)

        if self.verbose:
            print "Closing database connection"
        self.dbClose()