from nltk.sem.chat80 import country

from BotFinal_healthcare import *
import pyttsx3
import datetime
import speech_recognition as sr
import os
from googletrans import Translator
from gtts import gTTS
from playsound import playsound

myName="robo"
lang=' '

def wishme(lang):
    hour = datetime.datetime.now().hour
    if hour>=0 and hour<=12:
        chatbot_resp('Good Morning',lang)
    elif hour>12 and hour<18:
        chatbot_resp('Good Afternoon',lang)
    else:
        chatbot_resp('Good evening',lang)
    chatbot_resp(f'Iam {myName}, Nice to meet you!',lang)


def userSelectLanguage():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        #audio = r.listen(source)
        audio = r.listen(source, None, 10)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio,language='en-in')

            print('You Said:',query)
        except Exception:
            print('Say that again, please')
            return "Say Again",1
        return query,0

if __name__ == "__main__":
    i=1
    while i==1:
        chatbot_resp("Tell your language: Hindi or Telugu or English!","en")
        lang,i=userSelectLanguage()
        print(lang)
        if 'hindi' in lang.casefold():
            print('Hindi')
            lang='hi'
        elif 'telugu' in lang.casefold():
            print('Telugu')
            lang='te'
        elif 'english' in lang.casefold():
            print('English')
            lang='en'
        else:
            i=1

    print('The selected language by the user is:'+lang)
    wishme(lang)
    i=1
    while i==1:
        chatbot_resp("Do you want to know your health?Say (yes or no)",lang)
        resp,i = user_resp(lang)
        if resp == 'yes' or resp=='Yes' or resp=="Yeah" or resp=="yup" or resp=="yeah" or resp=="Yup": #change here
            getSeverityDict()
            getDescription()
            getprecautionDict()
            getInfo(lang)
            tree_to_code(clf, cols, lang)
        elif resp=='no' or resp=='No' or resp=='Nope' or resp == 'I do not know':
            chatbot_resp("Do you want to know the weather forecast of your city?Say (yes or no)",lang)
            resp, i = user_resp(lang)
            print(resp)
            if 'yes' in resp or 'Yes' in resp:
                chatbot_resp("Welcome to Weather forecast Chatbot!",lang)
                import requests
                import calendar

                api_key = 'ad62ecebb7931902c9fdbfefb78f3277'
                api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key

                running = True

                # chatbot_resp('Welcome..5 days weather forecast application using OpenWeatherMap\'s API!',lang)

                # Program loop
                while running:
                    i = 1
                    while i == 1:
                        chatbot_resp('Please input the city name: ', lang)
                        city, i = user_resp(lang)
                        if city.lower() == 'sf':
                            city = 'San Francisco, US'
                        api_call += '&q=' + city

                    # Stores the Json response
                    json_data = requests.get(api_call).json()

                    location_data = {
                        'city': json_data['city']['name'],
                        'country': json_data['city']['country']
                    }
                    #str = city + country
                    #chatbot_resp(city+country, lang)
                    print('\n{city}, {country}'.format(**location_data))
                    i=1
                    while i==1:
                        #chatbot_resp("Your choice. Say A - for knowing todays weather, Say B - for knowing next days weather",lang)
                        resp,i=user_resp(lang)
                        if 'A' in resp or "today's" in resp or 'today' in resp or 'a' in resp:
                            from datetime import datetime

                            date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
                            print(date_time)
                            api_key1 = 'ad62ecebb7931902c9fdbfefb78f3277'
                            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(
                                city, api_key1)
                            res = requests.get(url)
                            data = res.json()
                            print(f"Place : {data['name']}")
                            latitude = data['coord']['lat']
                            longitude = data['coord']['lon']
                            print('latitude :', latitude)
                            print('longitude :', longitude)
                            # getting the main dict block
                            main = data['main']
                            wind = data['wind']
                            # getting temperature
                            temperature = main['temp']
                            # getting the humidity
                            humidity = main['humidity']
                            tempmin = main['temp_min']
                            tempmax = main['temp_max']
                            # getting the pressure
                            windspeed = wind['speed']
                            pressure = main['pressure']
                            # weather report
                            report = data['weather']
                            chatbot_resp(f"Temperature : {temperature}°C",lang)
                            chatbot_resp(f"Temperature Min : {tempmin}",lang)
                            chatbot_resp(f"Temperature Max : {tempmax}",lang)
                            chatbot_resp(f"Humidity : {humidity}",lang)
                            chatbot_resp(f"Pressure : {pressure}",lang)
                            chatbot_resp(f"Wind Speed : {windspeed}",lang)
                            chatbot_resp(f"Weather Report : {report[0]['description']}",lang)
                        elif 'B' in resp or "tommorow's" in resp or 'tommorow' in resp or 'b' in resp:
                            i=1
                            while i==1:
                                chatbot_resp("Weather forecast of next how many days?Tell 0 to 5 days",lang)
                                num_days, i = user_resp(lang)  # defect code 2
                                # num={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20}
                                # num_days =int(num[num_days])
                                if "one".swapcase() in num_days or '1' in num_days:
                                    num_days = int(1)
                                elif "two".swapcase() in num_days or '2' in num_days:
                                    num_days = int(2)
                                elif "three" in num_days or '3' in num_days:
                                    num_days = int(3)
                                elif "four" in num_days or '4' in num_days:
                                    num_days = int(4)
                                elif "five" in num_days or '5' in num_days:
                                    num_days = int(5)
                                else:
                                    i=1
                            count=0
                            while count<num_days:
                                # The current date we are iterating through
                                current_date = ''
                                # Iterates through the array of dictionaries named list in json_data
                                for item in json_data['list']:
                                    print(count)
                                    # Time of the weather data received, partitioned into 3 hour blocks
                                    time = item['dt_txt']

                                    # Split the time into date and hour [2018-04-15 06:00:00]
                                    next_date, hour = time.split(' ')

                                    # Stores the current date and prints it once
                                    if current_date != next_date:
                                        current_date = next_date
                                        year, month, day = current_date.split('-')
                                        date = {'y': year, 'm': month, 'd': day}
                                        print('\n{d}/{m}/{y}'.format(**date))
                                        chatbot_resp(day + "-" + month + "-" + year, lang)

                                    # Grabs the first 2 integers from our HH:MM:SS string to get the hours
                                    hour = int(hour[:2])

                                    # Sets the AM (ante meridiem) or PM (post meridiem) period
                                    if hour < 12:
                                        if hour == 0:
                                            hour = 12
                                        meridiem = 'AM'
                                    else:
                                        if hour > 12:
                                            hour -= 12
                                        meridiem = 'PM'

                                    # Prints the hours [HH:MM AM/PM]
                                    chatbot_resp('\n%i:00 %s' % (hour, meridiem),lang)

                                    # Temperature is measured in Kelvin
                                    temperature = item['main']['temp']

                                    # Weather condition
                                    description = item['weather'][0]['description'],

                                    # Prints the description as well as the temperature in Celcius and Farenheit
                                    chatbot_resp('Weather condition: %s' % description, lang)
                                    chatbot_resp('Celcius: {:.2f}'.format(temperature - 273.15),lang)
                                    chatbot_resp('Farenheit: %.2f' % (temperature * 9 / 5 - 459.67),lang)
                                    count=count+1
                            # Prints a calendar of the current month
                            calender = " "
                            calendar = calendar.month(int(year), int(month))
                            print('\n' + calendar)
                        else:
                            i=1

                        # Asks the user if he/she wants to exit
                    while True:
                        running = input('Anything else we can help you with? ')
                        if running.lower() == 'yes' or running.lower() == 'y':
                            print('Great!')
                            break
                        elif running.lower() == 'no' or running.lower() == 'n' or running == 'exit':
                            print('Thanyesk you for using Jaimes Subroto\'s 5 day weather forecast application.')
                            print('Have a great day!')
                            running = False
                            break
                        else:
                            print('Sorry, I didn\'t get that.')

print("exited")
