# Setup database

## Basic configuration

### Create new DB and DB user

```
postgres=# CREATE USER user_name WITH PASSWORD 'password';
postgres=# CREATE DATABASE db_name WITH OWNER user_name;
postgres=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user_name;
```

### Add extension `pg_sphere`

See documentation https://pgsphere.github.io/doc/x46.html

```
git clone https://github.com/akorotkov/pgsphere.git
```

`pg_config` is required.

```
make USE_PGXS=1 PG_CONFIG=/usr/bin/pg_config

sudo make USE_PGXS=1 PG_CONFIG=/usr/bin/pg_config install
```

Then activate extension under superuser

```
sudo -u postgres psql -p db_port db_name

postgres=# create extension pg_sphere;
CREATE EXTENSION
```

### Add extension `q3c`

See https://github.com/segasai/q3c

...

```
postgres=# create extension q3c;
CREATE EXTENSION

postgres=# select q3c_version();
 q3c_version
-------------
 2.0.0
(1 row)
```

## Upload data

Prepare `sql`-script for loading data. See `upload_data.sql`.

Then login under db_user and upload data

```
psql -p db_port -U db_user db_name
\i upload_data.sql
```
