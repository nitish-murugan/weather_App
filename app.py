import datetime
from pprint import pprint
import json

from flask import Flask,render_template,redirect,session,request
import requests

app = Flask(__name__)
app.secret_key = "secretKey"

@app.route('/', methods=['GET', 'POST'])
def index():
    API_KEY = open("api_key.txt",'r').read()
    weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    #forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"

    if request.method == 'POST':
        city1 = request.form.get('city1')
        city2 = request.form.get('city2')
        print(city1,city2)
        
        weatherData1, forecastData1 = fetchData(city1,API_KEY,weather_url,forecast_url)
        #weatherData1, forecastData1 = json.load(open("weatherData.json",'r')), json.load(open("forecastData.json",'r'))
        
        if city2:
            weatherData2, forecastData2 = fetchData(city2,API_KEY,weather_url,forecast_url)
            #weatherData2, forecastData2 = json.load(open("weatherData.json",'r')), json.load(open("forecastData.json",'r'))
        else:
            weatherData2,forecastData2 = None, None
        
        return render_template("index.html", weatherData1=weatherData1, forecastData1=forecastData1, weatherData2=weatherData2, forecastData2=forecastData2)
    else:
        
        return render_template("index.html")

def fetchData(city, apiKey, weatherUrl, forecastUrl):
    weatherData = requests.get(weatherUrl.format(city,apiKey)).json()
    weatherInfo = {
        'name' : weatherData['name'],
        'temperature' : round(weatherData['main']['temp']-273.15,2),
        'description' : weatherData['weather'][0]['description'],
        'icon' : weatherData['weather'][0]['icon']
    }
    
    lat,lon = weatherData['coord']['lat'],weatherData['coord']['lat']
    forecastData = requests.get(forecastUrl.format(lat,lon,apiKey)).json()
    forecastInfo = []
    
    temp = []
    for i in forecastData['list']:
        day = datetime.datetime.fromtimestamp(i['dt']).strftime("%A")
        if day not in temp:
            temp.append(day)
            forecastInfo.append({
                'day' : day,
                'minTemp' : round(i['main']['temp_min']-273.15,2),
                'maxTemp' : round(i['main']['temp_max']-273.15,2),
                'description': i['weather'][0]['description'],
                'icon': i['weather'][0]['icon']
            })
    
    return weatherInfo, forecastInfo

if __name__ == "__main__":
    app.run(debug=True)