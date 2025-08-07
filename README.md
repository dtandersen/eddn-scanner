
Create `yoyo.ini`.

```
[DEFAULT]
sources = migrations
database = postgresql+psycopg://USERNAME:PASSWORD@localhost/scanner
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
