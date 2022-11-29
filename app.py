import os
import requests
from flask import Flask, request
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
WEATHERSTACK_API_KEY = os.environ.get('WEATHERSTACK_API_KEY')
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

app = Flask(__name__)

@app.route('/weather', methods=['POST'])
def weather():

    location = request.values.get('Body', '')
    messageRecipient = request.values.get('From', '')
    messageSender = request.values.get('To', '')

    client = Client(account_sid, auth_token)

    params = {
        'access_key': WEATHERSTACK_API_KEY,
        'query': location,
        'units': 'f',
    }

    api_result = requests.get('http://api.weatherstack.com/current', params)
    formatted_response = ''
    if api_result.status_code == 200:
        data = api_result.json()
        print(data)
        if data.get('error'):
            formatted_response = "Sorry, I am unable to get weather data for that location"
        else:
            weather_location = data['location']['name']
            temperature = data['current']['temperature']
            description = data['current']['weather_descriptions'][0]
            precipitation = data['current']['precip']
            uv_index = data['current']['uv_index']

            formatted_response = f'{weather_location}: {temperature}°, {description}. '

    else:
        formatted_response = "Sorry, I am unable to get the weather for that location."

    message = client.messages \
                .create(
                     body=formatted_response,
                     from_=messageSender,
                     to=messageRecipient
                 )

    return ""
    	
if __name__ == '__main__':
	app.run()


