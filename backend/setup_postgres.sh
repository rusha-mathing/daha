#!/bin/bash
set -e

DB_NAME="daha_db"
DB_USER="daha_user"
DB_PASSWORD="SWP2025"
PGDATA="/var/lib/postgres/data"

sudo apt update
sudo apt install -y postgresql postgresql-contrib

if [ ! -d "$PGDATA" ] || [ -z "$(ls -A $PGDATA)" ]; then
  sudo mkdir -p "$PGDATA"
  sudo chown -R postgres:postgres "$PGDATA"
  sudo -u postgres /usr/lib/postgresql/*/bin/initdb --locale=C.UTF-8 --encoding=UTF8 -D "$PGDATA"
fi

sudo systemctl enable postgresql
sudo systemctl restart postgresql

sudo -u postgres psql <<EOF
DO \$\$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_user WHERE usename = '${DB_USER}'
   ) THEN
      CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
   END IF;
END
\$\$;

CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
ALTER DATABASE ${DB_NAME} OWNER TO ${DB_USER};
EOF
