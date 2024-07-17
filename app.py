from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
API_KEY = os.getenv('OPEN_WEATHER_API')

@app.route('/')
def index():
    city = request.args.get('city', 'New York') 
    API_ENDPOINT = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'

    response = requests.get(API_ENDPOINT)
    data = response.json()
    

    # Extract relevant information from the response
    forecast = []
    for item in data['list']:
        # Check if it's a forecast for the next day
        if item['dt_txt'].split()[1] == '12:00:00':
            forecast.append({
                'date': item['dt_txt'],
                'temp': item['main']['temp']
            })

    # Get only the forecast for the next 7 days
    next_7_days = forecast[:7]

    return render_template('index.html', data={'forecast':next_7_days,'name':city})

if __name__ == '__main__':
    app.run(debug=True)
