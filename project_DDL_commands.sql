CREATE TABLE county (
county_name varchar(20) PRIMARY KEY,
number_of_evs int
);

CREATE TABLE zipcodes (
zipcode varchar(5),
median_income int,
households int,
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

CREATE TABLE charger (
charger_name varchar(100),
street varchar(50),
zipcode char(5),
ports int,
PRIMARY KEY(charger_name, street)
);

SELECT t.county_name, h.number_of_evs/t.traffic_count AS evs_per_traffic
FROM county h
JOIN traffic t ON h.county_name = t.county_name
ORDER BY evs_per_traffic DESC
LIMIT 1;


\copy county FROM 'csv/EV_Ownership_Data.csv' DELIMITER ',' CSV HEADER;
\copy traffic FROM 'csv/Traffic.csv' DELIMITER ',' CSV HEADER;
-- 250,000 salary are stored as a string and need to be handled in the future
\copy zipcodes FROM 'csv/nj-median-salary.csv' DELIMITER ',' CSV HEADER;
\copy zipcodes_nj FROM 'csv/zip_code_database_filtered.csv' DELIMITER ',' CSV HEADER;
\copy charger FROM 'csv/chargers.csv' DELIMITER ',' CSV HEADER;

CREATE VIEW zipcodes_and_county AS
SELECT zipcode, median_income, households, county
FROM zipcodes
NATURAL JOIN zipcodes_nj;

CREATE VIEW zipcodes_and_salary AS
SELECT AVG(median_income) as median_income, county
FROM zipcodes_and_county
GROUP BY county;

CREATE VIEW zipcodes_with_ev AS
SELECT median_income, county, number_of_evs
FROM zipcodes_and_salary AS Z
JOIN county AS C ON Z.county=C.county_name;

CREATE VIEW EV_Percentage_by_County AS
SELECT 
  c.county_name, 
  c.number_of_evs AS Total_EVs, 
  SUM(z.households) AS Total_Households, 
  AVG(z.median_income) AS Avg_Median_Salary, 
  (CAST(c.number_of_evs AS FLOAT) / CAST(SUM(z.households) AS FLOAT)) AS EV_Percentage
FROM 
  county c
  JOIN zipcodes_nj cz ON c.county_name = cz.county
  JOIN zipcodes z ON cz.zipcode = z.zipcode
WHERE 
  z.households <> 0
GROUP BY 
  c.county_name;

-- Call the seeding commands
-- \i project_DML_commands.sql
