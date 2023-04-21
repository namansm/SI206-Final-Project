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
    cur.execute("SELECT c.name, w.temperature, w.wind, w.rain FROM weather w INNER JOIN Countries c ON w.country_id = c.id")
    data = cur.fetchall()
    print(data)


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
<<<<<<< HEAD
    plt.savefig('india_temp_vs_cases.png')
=======
    plt.savefig('india_temp_vs_cases.png')


def main():
    cur, conn = open_database("covid_weather.db")
    calc_and_write_averages("output_data.csv", cur, conn)


if __name__ == '__main__':
    main()
>>>>>>> 6ad6db02e8fd2a38b7da706a9ea7b462775aea5a
