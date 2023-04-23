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
    
    # print(county_option)
    # for county in county_option:
    #     print(county[0])
    # print(year_option)
    
    return render_template('my-form.html', county_option=county_option, year_option=year_option)

# handle query POST and serve result web page
@app.route('/query-handler', methods=['POST'])
def query_handler():
    rows = connect(request.form['query'])
    return render_template('my-result.html', rows=rows)

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

@app.route('/charger-handler', methods=['POST'])
def charger_handler():
    county = request.form['county']
    query = f"SELECT county_name, charger_name, number_of_evs FROM (County AS C JOIN Charger AS Ch ON c.county_name=ch.county) WHERE county_name='{county}';"
    rows = connect(query)
    heads = ['County Name', 'Charger Name','Latest Number of EVs in County']
    if rows:
        return render_template('my-result.html', rows=rows, heads=heads)
    else:
        return "No results found."

if __name__ == '__main__':
    app.run(debug = True)
