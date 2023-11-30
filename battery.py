#!/usr/bin/env python3

output_ex_1 = 'Battery 0: Not charging, 59%'
output_ex_2 = 'Battery 0: Discharging, 59%, discharging at zero rate - will never fully discharge.'
output_ex_3 = 'Battery 0: Charging, 59%, charging at zero rate - will never fully charge.'

import subprocess, re
test = subprocess.Popen(["acpi"], stdout=subprocess.PIPE)
output = test.communicate()[0].decode("utf-8")
# output = output_ex_3
# print('|' + output + '|', len(output))

if not output: # No battery on this pc!
    print('')
    exit()

output = output.split(': ')[1]
output = output.split(', ')

# print(output)

status = output[0]
level = output[1]

if status == 'Not charging': icon = ' ' + level
elif status == 'Charging': icon = '%{F#5FAD41}%{F-} ' + level
else:
    bat = re.findall(r'\d+', level)[0]
    perc = int(bat)
    # level_pos = round(int(bat) * 0.05)
    # icon = 'BAT' + str(int(bat) * 0.05) + ' ' + str(level_pos)
    battery_0 = ''
    battery_1 = ''
    battery_2 = ''
    battery_3 = ''
    battery_4 = ''
    if perc < 13: icon = '%{F#E76F51}' + battery_0 + '%{F-}'
    elif perc < 38:  icon = '%{F#F4A261}' + battery_1 + '%{F-}'
    elif perc < 63:  icon = '%{F#E9C46A}' + battery_2 + '%{F-}'
    elif perc < 88:  icon = '%{F#9BAD42}' + battery_3 + '%{F-}'
    else:  icon = '%{F#5FAD41}' + battery_4 + '%{F-}'
    icon += ' ' + level
    #icon = [battery_0, battery_1, battery_2, battery_3, battery_4][level_pos] + ' ' + str(level)

print(icon)

#from time import sleep
#for i in range(5):
#    print(i, flush=True)
#    sleep(1)