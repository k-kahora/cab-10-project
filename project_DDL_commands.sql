CREATE TABLE county (
county_name varchar(20) PRIMARY KEY,
number_of_evs varchar(10)
);


CREATE TABLE zipcodes (
zipcode varchar(5),
median_income int,
num_of_houses int,
PRIMARY KEY(zipcode)
);

CREATE TABLE zipcodes_nj (
county varchar(20),
zipcode varchar(5),
PRIMARY KEY(zipcode)
);

CREATE TABLE traffic (
county_name varchar(20),
traffic_count int,
year char(4),
PRIMARY KEY(county_name, year),
FOREIGN KEY(county_name) REFERENCES county(county_name)
);

CREATE TABLE charger_type (
charger_name varchar(50) PRIMARY KEY,
level_one BOOLEAN,
level_two BOOLEAN,
dc_fast_charging BOOLEAN
);

CREATE TABLE charger (
charger_name varchar(50),
street varchar(50),
county varchar(20),
zipcode char(5),
ports int,
price float,
PRIMARY KEY(charger_name, street),
FOREIGN KEY(county) REFERENCES county(county_name),
FOREIGN KEY(charger_name) REFERENCES charger_type(charger_name));

\copy county FROM 'EV_Ownership_Data.csv' DELIMITER ',' CSV HEADER;
\copy traffic FROM 'Traffic.csv' DELIMITER ',' CSV HEADER;
-- 250,000 salary are stored as a string and need to be handled in the future
\copy zipcodes FROM 'nj-median-salary.csv' DELIMITER ',' CSV HEADER;
\copy zipcodes_nj FROM 'zip_code_database_filtered.csv' DELIMITER ',' CSV HEADER;

CREATE VIEW zipcodes_and_county AS
SELECT zipcode, median_income, num_of_houses, county
FROM zipcodes
NATURAL JOIN zipcodes_nj;


CREATE VIEW zipcodes_and_salary AS
SELECT AVG(median_income) as median_income, county
FROM zipcodes_and_county
GROUP BY county;


CREATE VIEW zipcodes_with_ev AS
SELECT median_income, county, number_of_evs
FROM zipcodes_and_salary
NATURAL JOIN county;

-- SELECT county, median_income
-- FROM zipcodes_and_salary
-- ORDER BY
-- ABS(median_income - %s)
-- ASC

-- Call the seeding commands
\i project_DML_commands.sql
