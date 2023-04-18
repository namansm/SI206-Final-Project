import requests
import json
import os
import time
import re
import sqlite3
import matplotlib as plt


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_covid_data(cur, conn):
    cur.execute("SELECT * FROM Covid")
    data = cur.fetchall()

    d = []

    for da in data:
        temp = {}
        temp["case_id"] = da[0]
        temp["country_id"] = da[1]
        temp["latitude"] = da[2]
        temp["longitude"] = da[3]
        temp["date"] = da[4]

        d.append(temp)

    return d


# Data should be a list of dictionaries
def load_weather_data(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS weather (case_id INTEGER PRIMARY KEY, country_id INTEGER, month INTEGER, temperature REAL, wind REAL, rain REAL)")

    url = "https://meteostat.p.rapidapi.com/point/daily"

    headers = {
        "X-RapidAPI-Key": "72117917afmsh2f97c3d988f6f27p1c320ajsn11aee594d295",
        "X-RapidAPI-Host": "meteostat.p.rapidapi.com"
    }

    count = 0
    ind = 0
    cur.execute("SELECT * FROM weather")
    prev_len = len(cur.fetchall())

    cur.execute("SELECT latitude, longitude FROM Covid WHERE country_id=?", (1,))
    ind_locs = cur.fetchall()[0]
    cur.execute("SELECT latitude, longitude FROM Covid WHERE country_id=?", (2,))
    sui_locs = cur.fetchall()[0]

    # THIS SECTION ONLY EXISTS BECAUSE WE NEEDED TO ACCOMODATE API BASIC RATE
    locs = {}
    
    params = {"lat":ind_locs[0],"lon":ind_locs[1],"start":"2020-03-01","end":"2021-03-31"}
    response = requests.get(url, headers=headers, params=params)
    res = response.json()["data"]
    for i in range(0, len(res)):
        mon = int(res[i]["date"][5:7])
        if(res[i]["date"][0:4] == "2021"):
            mon = mon + 12
        locs[i] = (1, res[i], mon)
    l = len(res)

    params = {"lat":sui_locs[0],"lon":sui_locs[1],"start":"2020-03-01","end":"2021-03-31"}
    response = requests.get(url, headers=headers, params=params)
    res = response.json()["data"]
    for i in range(0, len(res)):
        mon = int(res[i]["date"][5:7])
        if(res[i]["date"][0:4] == "2021"):
            mon = mon + 12
        locs[i+l] = (2, res[i], mon)
    # END SECTION

    while count < 25 and ind < len(locs):

        d = locs[ind]
        
        # THIS WOULD BE THE REQUEST PART WITHOUT THE API BASIC RATE
        # D IS DATA
        # params = {"lat":d["latitude"],"lon":d["longitude"],"start":d["date"],"end":d["date"]}
        # response = requests.get(url, headers=headers, params=params)
        # weather = response.json()["data"]

        cur.execute("INSERT OR IGNORE INTO weather (case_id, country_id, month, temperature, wind, rain) VALUES (?,?,?,?,?,?)", (ind, d[0], d[2], d[1]["tavg"], d[1]["wspd"], d[1]["prcp"],))

        cur.execute("SELECT * FROM weather")
        new_len = len(cur.fetchall())

        if prev_len == new_len:
            
            ind += 1
            continue

        prev_len = new_len
        count += 1
        ind += 1

    conn.commit()

def main():
     cur, conn = open_database('covid_weather.db')
     data = get_covid_data(cur, conn)
     load_weather_data(data, cur, conn)

if __name__ == '__main__':
    main()