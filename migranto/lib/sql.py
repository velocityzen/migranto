sqlite = {
    'createTable': """
            CREATE TABLE {tablename}
            (
              "name" text PRIMARY KEY,
               migration int,
              "timestamp" timestamp not null
            );
        """,
    'insertMigration': "INSERT INTO {tablename} (name, migration, timestamp) VALUES (?, 0, time('now') );",
    'updateMigration': "UPDATE {tablename} SET migration = ?, timestamp = time('now') WHERE name=?;",
    'selectLatestMigration': "SELECT migration FROM {tablename} WHERE name=?;",
    'selectAllMigrationStatus': "SELECT * FROM {tablename};",
    'selectOneMigrationStatus': "SELECT * FROM {tablename} WHERE name=?;",
}

pgsql = {
    'createTable': """
                CREATE TABLE {tablename}
                (
                  "name" text PRIMARY KEY,
                   migration int,
                  "timestamp" timestamp not null
                );
            """,
    'insertMigration': "INSERT INTO {tablename} (name, migration, timestamp) VALUES (%s, 0, NOW() );",
    'updateMigration': "UPDATE {tablename} SET migration=%s, timestamp = NOW() WHERE name=%s;",
    'selectLatestMigration': "SELECT migration FROM {tablename} WHERE name=%s;",
    'selectAllMigrationStatus': "SELECT * FROM {tablename};",
    'selectOneMigrationStatus': "SELECT * FROM {tablename} WHERE name=%s;",
}