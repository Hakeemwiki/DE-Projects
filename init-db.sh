#!/bin/bash
echo "Starting database initialization at $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
if ! psql -U "$POSTGRES_USER" -d postgres -lqt | cut -d \| -f 1 | grep -qw "airflow"; then
    echo "Creating airflow database..."
    psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE airflow;"
    psql -U "$POSTGRES_USER" -d postgres -c "CREATE USER airflow WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';"
    psql -U "$POSTGRES_USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;"
    echo "Database 'airflow' created and user configured."
else
    echo "Database 'airflow' already exists."
fi
echo "Database initialization completed at $(date -u +'%Y-%m-%d %H:%M:%S UTC')"