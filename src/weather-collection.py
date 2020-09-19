weather-collection.py
import csv
from sense_hat import SenseHat
from datetime import datetime, date
from time import sleep
import psutil

sense = SenseHat()

temp = date(2020, 4, 20)
end_date = temp.strftime("%m/%d/%Y")

opened = False

red = [255,0,0]
red_square = [
red,red,red,red,red,red,red,red,
red,red,red,red,red,red,red,red,
red,red,red,red,red,red,red,red,
red,red,red,red,red,red,red,red,
red,red,red,red,red,red,red,red,
red,red,red,red,red,red,red,red,
red,red,red,red,red,red,red,red,
red,red,red,red,red,red,red,red
]

with open('weatherdata.csv', 'a', newline='') as dont_touch:
    non_writer = csv.writer(dont_touch) 
with open('weatherdata.csv', 'r', newline='') as just_look:
    reader = csv.reader(just_look) 
    empty_test = [row for row in reader] 
    if len(empty_test) == 0: 
        opened = False 
    else:
        opened = True 

with open('weatherdata.csv', 'a', newline='') as weatherfile:
    writer = csv.writer(weatherfile)
    sense.set_pixels(red_square)
    if opened == False: 
        writer.writerow(['Date','Time','Temp(F)','Relative Humditity(%)','Pressure(mb)','CPU Utilization(%)','Response Time(sec)'])
    while(True):
        now = datetime.now()
        current_date = now.strftime("%m/%d/%Y")
        current_time = now.strftime("%H:%M")

        response_time_initial = datetime.now()
        tempinC = sense.get_temperature()
        tempinF = round((tempinC * 1.8) + 32,1)
        humidity = round(sense.get_humidity(),1)
        pressure = round(sense.get_pressure(),1)
        response_time_final = datetime.now()

        CPU = psutil.cpu_percent()
        response_time = response_time_final - response_time_initial

        writer.writerow([current_date,current_time,tempinF,humidity,pressure,CPU,response_time.total_seconds()])
        weatherfile.flush()

        print('wrote data at %s'%(current_time))
        sense.clear()
        sleep(1200)

        if(current_date == end_date):
            break


