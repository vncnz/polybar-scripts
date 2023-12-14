#!/usr/bin/env python3

import signal, time
import sys
from datetime import datetime, timedelta
import urllib3, json
http = urllib3.PoolManager()

class MyTime:
    def __init__(self):
        self.value = None

    def add (self, step):
        if not step:
            self.value = None
        else:
            now = datetime.now()
            value = self.value or now.replace(second=0, microsecond=0, minute=0, hour=now.hour)+timedelta(hours=now.minute//30)
            # parsed_date = now.replace(second=0, microsecond=0, minute=0, hour=now.hour)+timedelta(hours=now.minute//30)
            self.value = value + timedelta(hours=step)
        self.fixValue()
    
    def fixValue (self):
        if self.value and self.value < datetime.now():
            self.value = None

    def format (self):
        if self.value:
            return self.value.strftime("%Y-%m-%dT%H:%M")
        return 'NOW'
    
    def isNow (self):
        return not self.value

hour = MyTime()
running = True
changed = True
next_timestamp = datetime.now() - timedelta(days=10)
meteo_data = None

def getWeatherData ():
    url = 'https://api.open-meteo.com/v1/forecast?latitude=45.457692&longitude=10.570684&current=temperature_2m,apparent_temperature,is_day,precipitation,rain,weather_code&hourly=temperature_2m,apparent_temperature,weather_code&timezone=auto&forecast_days=3'
    try:
        data = json.loads(http.request('GET', url).data)
        return data
        example = '''{
            'latitude': 45.44, 
            'longitude': 10.58, 
            'generationtime_ms': 0.2779960632324219, 
            'utc_offset_seconds': 3600, 
            'timezone': 'Europe/Rome', 
            'timezone_abbreviation': 'CET', 
            'elevation': 86.0, 
            'current_units': {'time': 'iso8601', 'interval': 'seconds', 'temperature_2m': '°C', 'apparent_temperature': '°C', 'is_day': '', 'precipitation': 'mm', 'rain': 'mm', 'weather_code': 'wmo code'}, 
            'current': {'time': '2023-12-13T12:45', 'interval': 900, 'temperature_2m': 8.2, 'apparent_temperature': 6.9, 'is_day': 1, 'precipitation': 0.0, 'rain': 0.0, 'weather_code': 61}, 
            'hourly_units': {'time': 'iso8601', 'temperature_2m': '°C', 'apparent_temperature': '°C', 'weather_code': 'wmo code'}, 
            'hourly': {
                'time': ['2023-12-13T00:00', '2023-12-13T01:00', '2023-12-13T02:00', '2023-12-13T03:00', '2023-12-13T04:00', '2023-12-13T05:00', '2023-12-13T06:00', '2023-12-13T07:00', '2023-12-13T08:00', '2023-12-13T09:00', '2023-12-13T10:00', '2023-12-13T11:00', '2023-12-13T12:00', '2023-12-13T13:00', '2023-12-13T14:00', '2023-12-13T15:00', '2023-12-13T16:00', '2023-12-13T17:00', '2023-12-13T18:00', '2023-12-13T19:00', '2023-12-13T20:00', '2023-12-13T21:00', '2023-12-13T22:00', '2023-12-13T23:00', '2023-12-14T00:00', '2023-12-14T01:00', '2023-12-14T02:00', '2023-12-14T03:00', '2023-12-14T04:00', '2023-12-14T05:00', '2023-12-14T06:00', '2023-12-14T07:00', '2023-12-14T08:00', '2023-12-14T09:00', '2023-12-14T10:00', '2023-12-14T11:00', '2023-12-14T12:00', '2023-12-14T13:00', '2023-12-14T14:00', '2023-12-14T15:00', '2023-12-14T16:00', '2023-12-14T17:00', '2023-12-14T18:00', '2023-12-14T19:00', '2023-12-14T20:00', '2023-12-14T21:00', '2023-12-14T22:00', '2023-12-14T23:00', '2023-12-15T00:00', '2023-12-15T01:00', '2023-12-15T02:00', '2023-12-15T03:00', '2023-12-15T04:00', '2023-12-15T05:00', '2023-12-15T06:00', '2023-12-15T07:00', '2023-12-15T08:00', '2023-12-15T09:00', '2023-12-15T10:00', '2023-12-15T11:00', '2023-12-15T12:00', '2023-12-15T13:00', '2023-12-15T14:00', '2023-12-15T15:00', '2023-12-15T16:00', '2023-12-15T17:00', '2023-12-15T18:00', '2023-12-15T19:00', '2023-12-15T20:00', '2023-12-15T21:00', '2023-12-15T22:00', '2023-12-15T23:00'],
                'temperature_2m': [6.6, 6.9, 7.0, 7.2, 7.1, 6.9, 6.8, 6.9, 6.8, 7.0, 7.2, 7.3, 7.9, 8.3, 8.4, 8.0, 8.1, 7.7, 7.4, 7.4, 7.3, 7.1, 6.9, 6.6, 6.0, 5.6, 5.2, 4.6, 4.7, 4.8, 4.8, 4.2, 3.9, 4.4, 4.9, 6.2, 7.7, 8.8, 9.0, 9.2, 8.3, 6.7, 5.9, 5.7, 4.8, 4.4, 4.7, 5.2, 5.2, 6.3, 6.7, 6.6, 7.1, 6.4, 5.9, 6.1, 5.1, 5.6, 7.5, 8.6, 10.9, 11.8, 12.0, 11.5, 10.4, 8.6, 7.3, 6.2, 5.8, 5.7, 5.3, 5.2],
                'apparent_temperature': [5.5, 5.7, 5.6, 6.0, 5.3, 5.2, 5.3, 5.5, 4.8, 5.5, 4.8, 5.7, 6.3, 7.0, 7.0, 7.0, 6.8, 6.4, 5.6, 6.1, 6.0, 5.7, 5.2, 4.3, 3.9, 3.6, 3.3, 2.6, 2.9, 3.0, 2.7, 1.9, 1.7, 2.3, 3.0, 4.1, 5.9, 6.8, 6.7, 7.1, 6.1, 4.5, 3.7, 3.6, 2.5, 2.0, 2.4, 2.5, 2.6, 3.8, 4.4, 4.1, 4.7, 3.7, 3.4, 3.4, 2.1, 2.7, 5.0, 6.7, 8.6, 9.7, 9.6, 9.4, 8.7, 6.8, 5.5, 4.3, 3.9, 3.8, 3.2, 3.2],
                'weather_code': [61, 61, 61, 61, 61, 45, 61, 61, 61, 63, 63, 61, 61, 61, 61, 61, 61, 80, 3, 3, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1]
            }
        }'''
    except:
        return None

def printMeteoData ():
    try:
        if not hour.isNow():
            idx = meteo_data['hourly']['time'].index(hour.format())
            units = meteo_data['hourly_units']
            to_show = { 'is_day': True }
            for k,v in meteo_data['hourly'].items(): to_show[k] = v[idx]
            timestr = meteo_data['hourly']['time'][idx]
        else:
            units = meteo_data['current_units']
            to_show = meteo_data['current']
            timestr = 'NOW'

        weather_codes = {
            0: to_show['is_day'] and '' or '', # 'Clear sky',
            1: to_show['is_day'] and '' or '', # 'Mainly clear',
            2: to_show['is_day'] and '' or '', # 'Partly cloudy',
            3: '', # 'Overcast',
            45: '', # 'Fog',
            48: 'Depositing rime fog',

            51: '1', # 'Drizzle (light)',
            53: '2', # 'Drizzle (moderate)',
            55: '3', # 'Drizzle (dense)',

            56: 'Freezing drizzle (light)',
            57: 'Freezing drizzle (dense)',

            61: '', # 'Rain (slight)',
            63: '', # 'Rain (moderate)',
            65: '', # 'Rain (heavy)',

            66: 'Freezing rain (slight)',
            67: 'Freezing rain (heavy)',

            71: '1', # 'Snow (slight)',
            73: '2', # 'Snow (moderate)',
            75: '3', # 'Snow (heavy)',

            77:	'Snow grains',

            80: '1', # 'Rain showers (slight)',
            81: '2', # 'Rain showers (moderate)',
            82: '3', # 'Rain showers (violent)',

            85: 'Snow showers (slight)',
            86: 'Snow showers (heavy)',

            95: '', # 'Thunderstorm',
            96: '1', # 'Thunderstorm with slight hail',
            99: '2', # 'Thunderstorm with heavy hail'
            # 95 *	Thunderstorm: Slight or moderate
            # 96, 99 *	Thunderstorm with slight and heavy hail
        }
        
        temp = f"{round(to_show['apparent_temperature'])}{units['apparent_temperature']}"
        weather = to_show['weather_code']
        string_weather = weather_codes[weather]
        print(timestr + ' %{F#F0C674}' + string_weather + '%{F-} ' + str(temp), flush=True)
    except Exception as e:
        print('%{F#FF8080}%{F-}', flush=True)
        import sys
        print(data, file = sys.stderr)
        import traceback
        traceback.print_exc()

def signal_handler_usr1(sig, frame):
    # print(f'{sig} {frame}', flush=True)
    # print('Signal USR1', flush=True)
    hour.add(1)
    # global changed
    # changed = True
    printMeteoData()
    with open('meteo_log.txt', 'a') as file: file.write('time set to ' + hour.format() + '\n')
    # sys.exit(0)
def signal_handler_usr2(sig, frame):
    # print(f'{sig} {frame}', flush=True)
    # print('Signal USR2', flush=True)
    hour.add(-1)
    # global changed
    # changed = True
    printMeteoData()
    with open('meteo_log.txt', 'a') as file: file.write('time set to ' + hour.format() + '\n')
    # sys.exit(0)
def signal_handler_usr3(sig, frame):
    # print(f'{sig} {frame}', flush=True)
    print('Exiting...', flush=True)
    with open('meteo_log.txt', 'a') as file: file.write('Exiting\n')
    global running
    running = False
    sys.exit(0)

signal.signal(signal.SIGUSR1, signal_handler_usr1)
signal.signal(signal.SIGUSR2, signal_handler_usr2)
signal.signal(signal.SIGTERM, signal_handler_usr3)
# print('Started', flush=True)

while running:
    # signal.pause()
    if next_timestamp < datetime.now():
        # print('New net update')
        data = getWeatherData()
        if data:
            meteo_data = data
            next_timestamp = datetime.now() + timedelta(minutes=10)
            with open('meteo_log.txt', 'a') as file:
                file.write('weather updated at ' + datetime.now().strftime("%Y-%m-%dT%H:%M") + '\n')
            changed = True

    if changed:
        # print(hour.format())
        printMeteoData()
        changed = False
    time.sleep(60)