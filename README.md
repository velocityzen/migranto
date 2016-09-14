# Migranto
Simple SQL migration tool for SQLite and PostgreSQL

## Installation

    pip install migranto
    
or, if you intend to patch PostgreSQL databases:

    pip install migranto[PostgreSQL]

## Migrations

All migrations exist in one directory with names like:

	0001_some_useful_name.sql
	0001_some_useful_name_rollback.sql
	0002_some_other_useful_name.sql
	0002_some_other_useful_name_rollback.sql

Migranto checks the migrations directory and applies sql files to a database.
That's it. Simple enough.

## Usage:

`migranto [-h] --database URL [--storage NAME] [--name NAME] `

shows migrations status

`migranto [-h] --database URL --name NAME --path PATH [--migration N] [--storage NAME] [--verbose] [--fake] [--out] `

*	__--help, -h__ — show this help message and exit
*	__--database URL, -d URL__ — database url (pgsql://user:password@host:port/dbname or sqlite://path/to/data.base)
*	__--name NAME, -n NAME__ — migration set name
*	__--path PATH, -p PATH__ — path to migrations dir
*	__--migration N, -m N__ — migration step (last migration if omitted, 0 - before first migration)
*	__--storage NAME, -s NAME__ — migranto table name for data (default is migranto)
*	__--verbose, -v__ — verbose mode
*	__--out, -o__ — output sql to standard output, nothing applied to database.
*	__--fake, -f__ — fake migration (no sql applied to database, except migration number)
