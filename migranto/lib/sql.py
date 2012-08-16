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
    'updateMigration': "UPDATE {tablename} SET migration = ? WHERE name='?';",
    'selectLatestMigration': "SELECT migration FROM {tablename} WHERE name=?;",
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
    'updateMigration': "UPDATE {tablename} SET migration=%s WHERE name=%s;",
    'selectLatestMigration': "SELECT migration FROM {tablename} WHERE name=%s;",
}