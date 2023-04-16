import requests
import json
import os
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

    return data


def load_weather_data(data):
    url = "https://meteostat.p.rapidapi.com/point/daily"

    params = {"lat":"-33.77","lon":"18.56","start":"2020-01-01","end":"2020-01-31"}

    headers = {
        "X-RapidAPI-Key": "09dff8466dmsh2dcda9bcb212375p1bc56ejsn43f15c65bb68",
        "X-RapidAPI-Host": "meteostat.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)

    # MAKE SURE TO HAVE CONTINGENCY FOR EMPTY DATA JSON
    print(response.json())


def main():
     cur, conn = open_database('covid_weather.db')
     data = get_covid_data(cur, conn)
     load_weather_data(data)

if __name__ == '__main__':
    main()