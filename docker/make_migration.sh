#!/bin/bash

# Check if a comment argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <migration_comment>"
  exit 1
fi

MIGRATION_COMMENT=$1

# Step 1: Start the database container
docker-compose up -d database

# Step 2: Wait for the database to be ready
echo "Waiting for the database to be ready..."
while ! docker exec -i $(docker-compose ps -q database) pg_isready -U postgres -d my_db; do
  sleep 1
done

# Step 3: Run Alembic revision command
echo "Running alembic revision with comment: $MIGRATION_COMMENT"
cd ../src
alembic revision --autogenerate -m "$MIGRATION_COMMENT"
cd ../docker

# Step 4: Stop and remove the database container
echo "Stopping and removing the database container..."
docker-compose down