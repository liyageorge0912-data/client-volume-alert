# Client Volume Alert System

## Problem
In e-commerce marketing, operations teams have no automatic way to know 
if a client has zero or low campaign volume on a given day. The only way 
to find out is to manually open a dashboard and check each client one by 
one — which is time consuming and easy to miss. Zero volume usually means 
something has gone wrong with targeting setup or the data pipeline.

## Solution
A Python script that runs automatically every morning, queries a PostgreSQL 
database, aggregates campaign volume per client for the day, flags any client 
with zero or low volume, and sends an HTML table summary to the team email — 
removing the need to manually check any dashboard.

## How it works
1. query_data.py connects to PostgreSQL and counts customer rows per client for today
2. detect_issues.py flags clients with zero volume or below the minimum threshold
3. send_email.py sends an HTML table email — red rows for zero volume, yellow for low
4. main.py runs all three steps in order
5. Windows Task Scheduler triggers main.py every morning at 7am automatically

## Tech stack
- Python
- PostgreSQL
- psycopg2 — connects Python to PostgreSQL
- pandas — handles data as tables
- smtplib — sends emails via Gmail SMTP
- Windows Task Scheduler — runs the script daily

## Database structure
Three tables joined via SQL to produce daily volume per client:

- clients — one row per client
- campaigns — one row per campaign, linked to client
- campaign_targets — one row per customer per campaign per day

Volume is calculated by counting customer rows per client per day.
A client with zero rows has zero volume.

## How to run

### Setup — run once
```
python src/create_database.py
```

### Daily run
```
python src/main.py
```

## Configuration
All settings are stored in src/config.py:
- Database credentials
- Gmail credentials  
- VOLUME_THRESHOLD — minimum acceptable volume per client (default 50)

Note: config.py is excluded from GitHub via .gitignore to protect credentials.

## Sample output
The daily email shows a table like this:

| Client | Volume | Issue |
|---|---|---|
| SportGear Direct | 0 | Zero volume |
| KidsWear Boutique | 0 | Zero volume |
| TechAccessories Co | 26 | Low volume |
| OutdoorAdventure Ltd | 32 | Low volume |
```
