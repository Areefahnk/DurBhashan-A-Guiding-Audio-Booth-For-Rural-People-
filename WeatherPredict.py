import requests
import calendar

api_key = 'ad62ecebb7931902c9fdbfefb78f3277'
api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key

running = True

print('Welcome..5 days weather forecast application using OpenWeatherMap\'s API!')

# Program loop
while running:

    # Asks the user for the city or zip code to be queried
    while True:
        while True:

            # Input validation
            try:
                print('\nThis application supports search by city(0) or search by zip code(1).')
                search = int(input('Please input 0 or 1: '))
            except ValueError:
                print("Sorry, I didn't understand that.")
            else:

                # Passed the validation test
                if search == 0:
                    city = input('Please input the city name: ')
                    if city.lower() == 'sf':
                        city = 'San Francisco, US'

                    # Appends the city to the api call
                    api_call += '&q=' + city
                    break

                elif search == 1:
                    zip_code = input('Please input the zip code: ')

                    # Appends the zip code to the api call
                    api_call += '&zip=' + zip_code
                    break

                else:
                    # Prints the invalid number (not 0 or 1)
                    print('{} is not a valid option.'.format(search))