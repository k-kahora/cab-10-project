# CAB Project 10

Alex Quezada and Malcolm Kahora

## Document Wiki
Docs:
- [Phase I Initial Video](/docs/Phase1Proposal.mp4)
- [Phase II Proposal](/docs/PhaseIIProposal.pdf)
- [Phase III The Database Model Explained](/docs/PhaseIII-ERDiagram.pdf)
- [Phase III Elaboration: Datbase Model](/docs/PhaseIII-Schema.pdf)
- [Phase IV Elaboration: Database Design](/docs/PhaseIV-DBDesign.pdf)

## One-Time Installation

You must perform this one-time installation in the CSC 315 VM:

```
# install python pip and psycopg2 packages
sudo pacman -Syu
sudo pacman -S python-pip python-psycopg2

# install flask
pip install flask
```

## Usage

To populate the database, run the following script with sudo privileges:

```
sudo ./startup.sh
```

To run the Flask application, simply execute:

```
export FLASK_APP=app.py
flask run
# then browse to http://127.0.0.1:5000/
```

## Screenshots
![Home Page](images/home.png)  
![County Traffic Page](images/traffic.png)  
![Compare Median Income Page](images/median_salary.png)
![Chargers in County](images/county_chargers.png)
![All Chargers](images/all_chargers.png)
![EV:Household Ratio](images/ratio.png)



