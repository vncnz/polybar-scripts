#!/usr/bin/env python3
import urllib3, json
http = urllib3.PoolManager()

if __name__ == "__main__":
    url = 'https://api.open-meteo.com/v1/forecast?latitude=45.457692&longitude=10.570684&current=temperature_2m,apparent_temperature,is_day,precipitation,rain,weather_code&timezone=auto&forecast_days=1'
    try:
        data = json.loads(http.request('GET', url).data)
    except:
        print('')
        exit(0)
    # print(data)
    # example
    # https://open-meteo.com/en/docs#latitude=45.4713&longitude=10.5356&current=temperature_2m,apparent_temperature,is_day,precipitation,rain,weather_code&hourly=&timezone=auto&forecast_days=1
    # {'latitude': 45.46, 'longitude': 10.539999, 'generationtime_ms': 0.06198883056640625, 'utc_offset_seconds': 3600, 'timezone': 'Europe/Rome', 'timezone_abbreviation': 'CET', 'elevation': 93.0, 'current_units': {'time': 'iso8601', 'interval': 'seconds', 'temperature_2m': '°C', 'apparent_temperature': '°C', 'is_day': '', 'precipitation': 'mm', 'rain': 'mm', 'weather_code': 'wmo code'}, 'current': {'time': '2023-11-29T15:15', 'interval': 900, 'temperature_2m': 10.2, 'apparent_temperature': 7.0, 'is_day': 1, 'precipitation': 0.0, 'rain': 0.0, 'weather_code': 0}}
    try:
        units = data['current_units']
        current = data['current']

        weather_codes = {
            0: current['is_day'] and '' or '', # 'Clear sky',
            1: current['is_day'] and '' or '', # 'Mainly clear',
            2: current['is_day'] and '' or '', # 'Partly cloudy',
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
        
        temp = f"{round(current['apparent_temperature'])}{units['apparent_temperature']}"
        weather = current['weather_code']
        string_weather = weather_codes[weather]
        print('%{F#F0C674}' + string_weather + '%{F-} ' + str(temp))
    except Exception as e:
        print('%{F#FF8080}%{F-}')
        import sys
        print(data, file = sys.stderr)
        import traceback
        traceback.print_exc()