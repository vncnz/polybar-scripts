#!/bin/bash

url="https://api.open-meteo.com/v1/forecast?latitude=45.457692&longitude=10.570684&current=temperature_2m,apparent_temperature,is_day,precipitation,rain,weather_code&timezone=auto&forecast_days=1"

data=$(curl -s "$url")
if [$data -eq '']; then
    echo ''
else
    weather=$(echo $data | jq -r '.current.weather_code' )
    temp=$(echo $data | jq -r '.current.apparent_temperature' | awk '{print int($1+0.5)}')
    temp_unit=$(echo $data | jq -r '.current_units.apparent_temperature' )
    day=$(echo $data | jq -r '.current.is_day' )

    echo -n '%{F#F0C674}'
    if [ $weather -eq 0 ] && [ $day -eq 1 ]; then
        echo -n '' # Clear sky
    elif [ $weather -eq 0 ] && [ $day -eq 0 ]; then
        echo -n '' # Clear sky
    elif [ $weather -eq 1 ] && [ $day -eq 1 ]; then
        echo -n '' # Mainly clear
    elif [ $weather -eq 1 ] && [ $day -eq 0 ]; then
        echo -n '' # Mainly clear
    elif [ $weather -eq 2 ] && [ $day -eq 1 ]; then
        echo -n '' # Partly cloudy
    elif [ $weather -eq 2 ] && [ $day -eq 0 ]; then
        echo -n '' # Partly cloudy
    elif [ $weather -eq 3 ]; then
        echo -n '' # Overcast
    elif [ $weather -eq 45 ]; then
        echo -n '' # Fog
    elif [ $weather -eq 48 ]; then
        echo -n 'Depositing rime fog'
    elif [ $weather -eq 51 ]; then
        echo -n '1' # 'Drizzle (light)'
    elif [ $weather -eq 53 ]; then
        echo -n '2' # 'Drizzle (moderate)'
    elif [ $weather -eq 55 ]; then
        echo -n '3' # 'Drizzle (dense)'



    elif [ $weather -eq 56 ]; then
        echo -n 'Freezing drizzle (light)'
    elif [ $weather -eq 57 ]; then
        echo -n 'Freezing drizzle (dense)'

    elif [ $weather -eq 61 ]; then
        echo -n '' # 'Rain (slight)'
    elif [ $weather -eq 63 ]; then
        echo -n '' # 'Rain (moderate)'
    elif [ $weather -eq 65 ]; then
        echo -n '' # 'Rain (heavy)'

    elif [ $weather -eq 66 ]; then
        echo -n 'Freezing rain (slight)'
    elif [ $weather -eq 67 ]; then
        echo -n 'Freezing rain (heavy)'

    elif [ $weather -eq 71 ]; then
        echo -n '1' # 'Snow (slight)'
    elif [ $weather -eq 73 ]; then
        echo -n '2' # 'Snow (moderate)'
    elif [ $weather -eq 75 ]; then
        echo -n '3' # 'Snow (heavy)'

    elif [ $weather -eq 77 ]; then
        echo -n 'Snow grains'

    elif [ $weather -eq 80 ]; then
        echo -n '1' # 'Rain showers (slight)'
    elif [ $weather -eq 81 ]; then
        echo -n '2' # 'Rain showers (moderate)'
    elif [ $weather -eq 82 ]; then
        echo -n '3', # 'Rain showers (violent)'
    elif [ $weather -eq 85 ]; then
        echo -n 'Snow showers (slight)'
    elif [ $weather -eq 86 ]; then
        echo -n 'Snow showers (heavy)'

    elif [ $weather -eq 95 ]; then
        echo -n '' # 'Thunderstorm'
    elif [ $weather -eq 96 ]; then
        echo -n '1' # 'Thunderstorm with slight hail'
    elif [ $weather -eq 99 ]; then
        echo -n '2' # 'Thunderstorm with heavy hail'
    # 95 *	Thunderstorm: Slight or moderate
    # 96, 99 *	Thunderstorm with slight and heavy hail
    else
        echo -n $weather
    fi

    echo -n '%{F-}'
    echo '' $temp$temp_unit
fi