import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import re

#!/usr/bin/env python
# coding: utf-8
"""
Author: Coco Wang (kexinwan)
5 day weather forecast
"""

# Usage:
# location = "Duende, Buffalo, NY, US"
# [lat, lon] = getGeo(location)
# getWeather(lat, lon)


def getWeather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid=160944c43d077485a3939233eedcadf2"
    response = requests.get(url)
    data = json.loads(response.text)
    mainData = []
    for i in data['list']:
        temp = i['main']['temp']
        weather = i['weather'][0]['main']
        weatherDesc = i['weather'][0]['description']
        time = i['dt_txt']
        # datetime.strptime(date_string, format)
        if(re.search('00:00:00$', time)):
            time = time[:10]
            mainData.append([time, temp, weather, weatherDesc])
        
    weatherInfo = pd.DataFrame(data=mainData, columns=['time', 'temp', 'weather', 'weatherDesc'])
    # function 1: show weather information in the following 5 days.
    print(weatherInfo)

    # function 2: plot the temperature trend in the following 5 days.
    weatherInfo.plot(x='time',y='temp',style='.-')
    plt.show()
    return weatherInfo


def getGeo(place):
    if place == 'New York (NYC)':
        return [40.71, -74.00]
    url = f"http://api.positionstack.com/v1/forward?access_key=a7ce045bf4fd5bdcaa2273a2d412e4d2&query={place}"
    response = requests.get(url)
    data = json.loads(response.text)
    return [data['data'][0]['latitude'], data['data'][0]['longitude']]

    # from requests import get
    # from bs4 import BeautifulSoup
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',}
    # response = get("https://www.google.com/search?q=latitude+longitude+of+75270+postal+code+paris+france",headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # a = soup.find_all('div', {'class':'N6Sb2c i29hTd'})
    # print(a)
    
    # url = "https://www.google.com/search?q=latitude+longitude+of+nyc&ei=ZfVBY-HSMKOu5NoPhtqWMA&ved=0ahUKEwihmeKV09H6AhUjF1kFHQatBQYQ4dUDCA4&uact=5&oq=latitude+longitude+of+nyc&gs_lcp=Cgdnd3Mtd2l6EAMyCggAEEcQ1gQQsAMyCggAEEcQ1gQQsAMyCggAEEcQ1gQQsAMyCggAEEcQ1gQQsAMyCggAEEcQ1gQQsAMyCggAEEcQ1gQQsAMyCggAEEcQ1gQQsAMyCggAEEcQ1gQQsANKBAhBGABKBAhGGABQAFgAYN-fYGgCcAF4AIABAIgBAJIBAJgBAMgBCMABAQ&sclient=gws-wiz"
    # response = requests.get(url)

    # # Convert it to proper html
    # html = response.text
    # # Parse it in html document
    # soup = BeautifulSoup(html, 'html.parser')
    # # Grab the container and its content
    # target_container = soup.find("div", {"class": "Z0LcW t2b5Cf"})
    # print(target_container)
    