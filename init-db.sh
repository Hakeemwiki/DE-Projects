#!/bin/bash
# init-db.sh
# This script initializes the PostgreSQL database for Airflow.
# It creates the 'airflow' database and user if they do not already exist.

# Log the start of the database initialization process with a UTC timestamp
echo "Starting database initialization at $(date -u +'%Y-%m-%d %H:%M:%S UTC')"

# Check if the 'airflow' database exists
# Uses psql to list databases, filters for 'airflow', and checks if it exists
if ! psql -U "$POSTGRES_USER" -d postgres -lqt | cut -d \| -f 1 | grep -qw "airflow"; then
    # If the database does not exist, create it
    echo "Creating airflow database..."
    psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE airflow;"  # Create database
    psql -U "$POSTGRES_USER" -d postgres -c "CREATE USER airflow WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';"  # Create user
    psql -U "$POSTGRES_USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;"  # Grant privileges
    echo "Database 'airflow' created and user configured."
else
    # If the database already exists, log a message
    echo "Database 'airflow' already exists."
fi

# Log the completion of the initialization process with a UTC timestamp
echo "Database initialization completed at $(date -u +'%Y-%m-%d %H:%M:%S UTC')"