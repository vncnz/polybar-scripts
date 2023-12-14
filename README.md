# polybar-scripts
My polybar scripts in bash and python

## battery.sh
Bash script, uses Font Awesome 5 (or 6) Free to display icons and percentage:
- No battery, it shows a white electricity plug
- Charging battery, it shows a green electricity plug with a bolt badge and battery percentage
- Not charging battery, it shows a white electricity plug with a check badge and battery percentage
- Discharging battery, it shows a colored battery symbol (depending on charge) and percentage

## battery.py
Python script, equivalent of the bash one

## meteo.sh
Bash script, uses Font Awesome 5 (or 6) Free to display icon and apparent temperature of current weather

## meteo.py
Python script. It displays the current weather. By sending the USR1 or USR2 IPC signal, you can view forecasts. The USR1 signal increments the forecasted time, while USR2 decrements it by one hour per step. Decrementing until the present time resets the script to the current-time mode. When the forecasted time matches the current time while in forecast mode, the script automatically switches back to current-time mode.
This is an example of polybar configuration, allowing to change the time with left and right mouse click:
```
[module/weather]
type = custom/script
exec = /PATH/TO/SCRIPT/meteo.py 2>/dev/null
click-left = "kill -USR1 $(pgrep --oldest --parent %pid%)"
#scroll-up = "kill -USR1 $(pgrep --oldest --parent %pid%)"
#scroll-down = "kill -USR2 $(pgrep --oldest --parent %pid%)"
click-right = "kill -USR2 $(pgrep --oldest --parent %pid%)"
format = <label>
label = %output%
label-padding = 1
tail = true
```

It is important to note the flag `tail = true`: the script keeps running and keeps in memory the setting about what to show, updating displayed data only when necessary (every 10 minutes by network update and every USR1/USR2 event).