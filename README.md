# EDDN Scanner

A tool for Elite Dangerous that reads events from EDDN and saves them to a Postgres database.

# Running

Create `yoyo.ini`.

```
[DEFAULT]
sources = migrations
database = postgresql+psycopg://DB_USER:DB_PASSWORD@DB_HOST/DB_NAME
batch_mode = off
verbosity = 0
```

Create database with yoyo:

```
yoyo list
yoyo apply
```

.env

```
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=USERNAME
DB_PASSWORD=PASSWORD
DB_NAME=scanner
```
