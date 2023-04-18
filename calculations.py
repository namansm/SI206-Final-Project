import requests
import json
import os
import re
import sqlite3
import csv
import matplotlib as plt


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def calc_and_write_averages(outfile, cur, con):
    cur.execute("SELECT c.name, w.month, AVG(w.temperature), AVG(w.wind), AVG(w.rain) FROM weather w INNER JOIN Countries c ON w.country_id = c.id WHERE w.country_id=1 GROUP BY w.month")
    ind_data = cur.fetchall() 
    cur.execute("SELECT c.name, w.month, AVG(w.temperature), AVG(w.wind), AVG(w.rain) FROM weather w INNER JOIN Countries c ON w.country_id = c.id WHERE w.country_id=2 GROUP BY w.month")
    sui_data = cur.fetchall() 
    
    months = ["xx", "xx", "xx", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "January", "February", "March"]

    outFile = open(outfile, "w")
    csvOut = csv.writer(outFile)

    csvOut.writerow(("Country","Month","Average Daily Temperature (C)","Average Daily Wind Speed (kph)", "Average Daily Rainfall (mm)"))

    data = []
    data.extend(ind_data)
    data.extend(sui_data)
    for t in data:
        csvOut.writerow(t)

    return data



def plot_india_tempvscases(db):
    with open(db, 'r') as f:
        lines = f.readlines()

    result = {}
    for line in lines:
        splitLine = line.split(',')
        temperature = splitLine[0]
        cases = splitLine[1]
        result[temperature] = cases

    plt.bar(result.keys(), result.values())
    #plt.invert_y_axis()
    plt.set_title('Temperature vs Covid Cases in India')
    plt.xlabel('Temperature')
    plt.ylabel('Number of Cases')
    plt.savefig('india_temp_vs_cases.png')

def main():
     cur, conn = open_database('covid_weather.db')
     data = calc_and_write_averages("output.csv", cur, conn)

if __name__ == '__main__':
    main()