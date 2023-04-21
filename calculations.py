
#1 to 396: india
#397-792: switzerland


#1: group by month avgs , temperature of both countries x acis: month and y axis: temp
#2: select total num covid cases + total severe weather cases 


import requests
import json
import os
import re
import sqlite3
import csv
import matplotlib
import matplotlib.pyplot as plt


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


def plot_month_vs_temps(filename):

    f = open(filename, "r")
    allLines = f.readlines()

    india_months = []
    india_temps = []

    swiz_months = []
    swiz_temps = []

    f.close()
    months = ["xx", "xx", "xx", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "January", "February", "March"]

    for i in range(1, 13): #india
        splitLine = allLines[i].split(',')
        month = months[int(splitLine[1])]
        temp = float(splitLine[2])
        
        india_months.append(month)
        india_temps.append(round(temp,2))

    for i in range(14, 26): #swiz
        splitLine = allLines[i].split(',')
        month = months[int(splitLine[1])]
        temp = float(splitLine[2])
        
        swiz_months.append(month)
        swiz_temps.append(round(temp,2))

    plt.figure(figsize=(9,9))
    plt.plot(india_months, india_temps)
    plt.plot(swiz_months, swiz_temps)

    plt.title('Average Temperatures in India vs Switzerland per Month')
    plt.xlabel('Month')
    plt.xticks(rotation=45)
    plt.ylabel('Average Temperature (C)')
    plt.legend(["India", "Switzerland"])
    plt.savefig('month_vs_temp.png')

def calc_severe(cur, con):
    cur.execute("SELECT c.name, COUNT(w.wind) FROM weather w INNER JOIN Countries c ON w.country_id = c.id WHERE w.wind>65 OR w.temperature>35 OR w.temperature<0 OR w.rain>48 GROUP BY w.country_id")
    severe_data = cur.fetchall()
    
    cur.execute("SELECT c.name, MAX(cv.num_cases) FROM Covid cv INNER JOIN Countries c ON cv.country_id = c.id GROUP BY country_id")
    maxes = cur.fetchall()

    data = []
    for i in range(2):
        temp = (severe_data[i][0], severe_data[i][1], maxes[i][1])
        data.append(temp)
    
    return data


def plot_severe_vs_total_cases(data):
    ratios = []
    countries = []

    for country in data:
        ratios.append(float(country[1])/float(country[2]))
        countries.append(country[0])
        
    print(ratios)
    plt.figure(figsize=(9,9))
    plt.bar(countries, ratios, color='maroon')

    plt.title('Ratio of Severe Weather Covid Cases to Total Covid Cases per Country')
    plt.xlabel('Country')
    plt.ylabel('Ratio')
    plt.savefig('ratio_vs_country.png')


def main():
    cur, conn = open_database('covid_weather.db')
    data = calc_and_write_averages("output.csv", cur, conn)
    plot_month_vs_temps("output.csv")
    data2 = calc_severe(cur, conn)
    plot_severe_vs_total_cases(data2)


if __name__ == '__main__':
    main()