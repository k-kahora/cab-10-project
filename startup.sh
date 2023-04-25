#!/bin/bash

USER=test_user
PASSWORD=test_user
DATABASE=testdb

# Create the new user
psql -c "CREATE USER $USER WITH PASSWORD '$PASSWORD';"
CREATE USER test_user WITH PASSWORD 'test_user';

# login with the new user make the database and also populate it

psql -U $USER -d postgres <<EOF
-- Make the database
   CREATE DATABASE $DATABASE;
   CREATE DATABASE testdb

-- Switch to the database
   \c $DATABASE;

-- Load the database with the data
   \i project_DDL_commands.sql 

EOF


