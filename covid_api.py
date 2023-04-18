import requests
import json
import os
import re
import sqlite3
import matplotlib as plt

#db: country, lat, lon, date
#countries table w country id and name and lat lon


#fn made the req successfully and notified if sucess or not
#another fn takes that outfput and do a specific thing, such as getting one list
#tables individually, everything i can to store the info
# new py file to get the tables and perform calcs and make visualization


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    cur, conn = open_database('covid_weather.db')
    data = load_api_data()
    make_covid_table(data, cur, conn)
    

def load_api_data():
    '''
    Return a dictionary representation of the decoded JSON. 
    If the search is unsuccessful, print "Exception!" and return None.
    '''

    payload={}
    headers = {}

    response = requests.request("GET", 'https://api.covid19api.com/country/India/status/confirmed?from=2020-03-01T00:00:00Z&to=2021-03-31T00:00:00Z', headers=headers, data=payload)
    d = {}

    if (response.ok): 
        data = response.json()
        for i in range(0,len(data)):
            d[i] = data[i]
    else:
        print("Exception!")
        return None
    
    l = len(data)
    response = requests.request("GET", 'https://api.covid19api.com/country/switzerland/status/confirmed?from=2020-03-01T00:00:00Z&to=2021-03-31T00:00:00Z', headers=headers, data=payload)
    
    if (response.ok): 
        data = response.json()
        for i in range(0,len(data)):
            d[i+l] = data[i]
    else:
        print("Exception!")
        return None
    return d

def make_covid_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Covid (case_id INTEGER PRIMARY KEY, country_id INTEGER, latitude REAL, longitude REAL, date TEXT)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS Countries (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT OR IGNORE INTO Countries (id, name) VALUES (?, ?)", (1, 'India'))
    cur.execute("INSERT OR IGNORE INTO Countries (id, name) VALUES (?, ?)", (2, 'Switzerland'))
    conn.commit()

    ind = 0
    count = 0
    cur.execute("SELECT * FROM Covid")
    prev_len = len(cur.fetchall())

    while count < 25 and ind < len(data):
        d = data[ind]
        cur.execute("SELECT id FROM Countries WHERE name=?", (d["Country"],))
        country = cur.fetchall()[0][0]
        lat = d["Lat"]
        lon = d["Lon"]
        dates = d["Date"][0:10]
        
        cur.execute("INSERT OR IGNORE INTO Covid (case_id, country_id, latitude, longitude, date) VALUES (?,?,?,?,?)", (ind, country, lat, lon, dates))
        cur.execute("SELECT * FROM Covid")
        new_len = len(cur.fetchall())

        if prev_len == new_len:
            ind+=1
            continue

        prev_len = new_len
        count += 1
        ind += 1

    conn.commit()
        


if __name__ == '__main__':
    main()
