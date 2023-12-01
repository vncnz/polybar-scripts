#!/bin/bash

warn_on=20
debug=0

discharging=`acpi | grep Discharging | wc -l` # will be 1 if discharging and 0 otherwise
charging=`acpi | grep Charging | wc -l` # will be 1 if charging and 0 otherwise
stable=`acpi | grep "Not charging" | wc -l` # will be 1 if discharging and 0 otherwise
percentage_remaining=`acpi | grep -o [0-9]*% | sed s/%//g`

if [ $discharging -eq 1 ]; then # if discharging, check percentage
    # echo "Discharging ${percentage_remaining}%"
    if [ $percentage_remaining -lt 13 ]; then
        echo "%{F#E76F51}%{F-} ${percentage_remaining}%"
    elif [ $percentage_remaining -lt 38 ]; then
        echo "%{F#F4A261}%{F-} ${percentage_remaining}%"
    elif [ $percentage_remaining -lt 63 ]; then
        echo "%{F#E9C46A}%{F-} ${percentage_remaining}%"
    elif [ $percentage_remaining -lt 88 ]; then
        echo "%{F#9BAD42}%{F-} ${percentage_remaining}%"
    else
        echo "%{F#5FAD41}%{F-} ${percentage_remaining}%"
    fi

    if [ $percentage_remaining -lt $warn_on ]; then
        notify-send "Warning, battery is discharging and at ${percentage_remaining}%!"
    elif [ $debug -eq 1 ]; then
        notify-send "Battery is discharging, but at ${percentage_remaining}% so it's grand!"
    fi
elif [ $charging -eq 1 ]; then
    echo "%{F#5FAD41}%{F-} ${percentage_remaining}%"
elif [ $stable -eq 1 ]; then
    echo " ${percentage_remaining}%"
else
    echo "" # "No battery!"
fi