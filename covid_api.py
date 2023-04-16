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

def main():
    data = load_api_data('https://api.covid19api.com/live/country/south-africa/status/confirmed')
    cur, conn = open_database('covid_weather.db')
    make_covid_table(data, cur, conn)
    

def load_api_data(url, params=None):
    '''
    Return a dictionary representation of the decoded JSON. 
    If the search is unsuccessful, print "Exception!" and return None.
    '''

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if (response.ok): 
        print(response.text)
        return json.loads(response.text)
    else:
        print("Exception!")
        return None


def make_covid_table(data, cur, conn):
    countries = []
    for player in data['squad']:
        position = player['position']
        if position not in positions:
            positions.append(position)
    
    cur.execute("CREATE TABLE IF NOT EXISTS Covid (id INTEGER PRIMARY KEY, position TEXT UNIQUE)")

    for i in range(len(positions)):
        cur.execute("INSERT OR IGNORE INTO Covid (id, position) VALUES (?,?)",(i, positions[i]))
    conn.commit()



if __name__ == '__main__':
    main()