import requests
import json
import os
import re
import sqlite3
import matplotlib as plt

def calc_average_temp_india():
    pass


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
    pass

if __name__ == '__main__':
    main()