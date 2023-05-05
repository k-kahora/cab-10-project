#!/bin/bash

USER=test_user
PASSWORD=test_user
DATABASE=testdb

# Create the new user
sudo -u postgres psql -c "CREATE USER $USER WITH PASSWORD '$PASSWORD';"
sudo -u postgres psql -c "CREATE USER test_user WITH PASSWORD 'test_user';"
sudo -u postgres psql -c "CREATE DATABASE $DATABASE"

# psql -c "CREATE USER $USER WITH PASSWORD '$PASSWORD';"
# psql -c "CREATE USER test_user WITH PASSWORD 'test_user';"

# login with the new user make the database and also populate it

psql -U $USER -d $DATABASE <<EOF
-- Switch to the database

-- Load the database with the data
   \i project_DDL_commands.sql 

EOF


