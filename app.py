#! /usr/bin/python3

"""
This is an example Flask | Python | Psycopg2 | PostgreSQL
application that connects to the 7dbs database from Chapter 2 of
_Seven Databases in Seven Weeks Second Edition_
by Luc Perkins with Eric Redmond and Jim R. Wilson.
The CSC 315 Virtual Machine is assumed.

John DeGood
degoodj@tcnj.edu
The College of New Jersey
Spring 2020

----

One-Time Installation

You must perform this one-time installation in the CSC 315 VM:

# install python pip and psycopg2 packages
sudo pacman -Syu
sudo pacman -S python-pip python-psycopg2

# install flask
pip install flask

----

Usage

To run the Flask application, simply execute:

export FLASK_APP=app.py 
flask run
# then browse to http://127.0.0.1:5000/

----

References

Flask documentation:  
https://flask.palletsprojects.com/  

Psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query):
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    
    county_option = connect("SELECT county_name FROM County ORDER BY county_name ASC;")
    
    year_option = connect("SELECT DISTINCT year FROM traffic ORDER BY year DESC;")
    
    return render_template('my-form.html', county_option=county_option, year_option=year_option)

@app.route('/county-handler', methods=['POST'])
def county_handler():
    county = request.form['county']
    year = request.form['year']
    heads = ['County Name', 'Traffic Count', 'Year', 'Latest Number of EVs in County']
    
    if(county == "All"):
        query = f"SELECT county_name, traffic_count, year, number_of_evs FROM (County NATURAL JOIN Traffic) WHERE year='{year}';"
        rows = connect(query)
        return render_template('my-result.html', rows=rows, heads=heads)
    
    query = f"SELECT county_name, traffic_count, year, number_of_evs FROM (County NATURAL JOIN Traffic) WHERE county_name='{county}' AND year='{year}';"
    rows = connect(query)
    return render_template('my-result.html', rows=rows, heads=heads)

@app.route('/salary-handler', methods=['POST'])
def salary_handler():
    salary = request.form['salary']
    query = f"SELECT county, median_income, number_of_evs FROM zipcodes_with_ev ORDER BY ABS(median_income - '{salary}') ASC;"

    rows = connect(query)
    heads = ['County Name', 'Median Income', 'Number of EVs']
    if rows:
        return render_template('my-result.html', rows=rows, heads=heads)
    else:
        return "No results found."

@app.route('/percent-handler', methods=['POST'])
def percent_handler():
    query = f"SELECT * FROM EV_Percentage_by_County;"

    rows = connect(query)
    heads = ['County', 'Total EVs', 'Total Households', 'Average Median Salary', 'EVs per Household']
    if rows:
        return render_template('my-result.html', rows=rows, heads=heads)
    else:
        return "No results found."

@app.route('/county-ports', methods=['POST'])
def charger_port_handler():
    query = '''
SELECT z.county, MAX(c.ports)
FROM charger c, zipcodes_and_county z 
GROUP BY z.county;
'''
    #join togeth 
    all_chargers = '''
    SELECT *
    FROM charger;

    '''
    county_chargers = '''
    SELECT county, zipcode
    FROM zipcodes_and_county;
    '''

    county_chargers_one = '''
    SELECT c.charger_name, h.county, c.zipcode, c.street, c.ports 
    FROM charger c
    NATURAL JOIN zipcodes_and_county h;
    '''
    rows = connect(county_chargers_one)
    heads = ['Charger Name','County', 'Zipcode', 'Street Address', 'Number of Posts'] 
    if rows:
        return render_template('my-result.html', rows=rows, heads=heads)
    else:
        return "No results found."
    
@app.route('/charger-by-county', methods=['POST'])
def charger_county_handler():
    county = request.form['county']
    query = '''
SELECT h.county_name, c.charger_name, c.ports
FROM county h 
NATURAL JOIN charger c
WHERE h.county_name = '{0}'
'''.format(county)

    county_option = connect('''
    SELECT county_name
    FROM County
    ORDER BY county_name ASC;
    ''')

    rows = connect(query)
    heads = ['County', 'Charger Name', 'Ports'] 
    if rows:
        return render_template('my-result.html', county_option=county_option, rows=rows, heads=heads)
    else:
        return "No results found."

if __name__ == '__main__':
    app.run(debug = True, host="localhost", port="8080")
