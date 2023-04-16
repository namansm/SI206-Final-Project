import requests
import json
import re
import matplotlib as plt



def main():
    params = {'param': ['temperature','wind_speed'],
                         'start': '2010-01-01',
                         'end': '2018-12-31',
                         'lat': 43.6529,
                         'lon': -79.3849,}
    r = requests.get('https://api.oikolab.com/weather',params=params)
    print(r.text)


if __name__ == '__main__':
    main()