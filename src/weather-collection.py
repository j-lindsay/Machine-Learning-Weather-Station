weather-collection.py
import csv
from sense_hat import SenseHat
from datetime import datetime, date
from time import sleep
import psutil

#make SenseHat object
sense = SenseHat()

#make end date datetime object to end program
temp = date(2020, 4, 20)
end_date = temp.strftime("%m/%d/%Y")

#boolean to see if the file has been opened or not
opened = False

#set up led matrix to indicate the program is running
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


#open csv file and then read if it has already been written to (just in case the pi fails overnight I don't want the header to be written twice)
with open('weatherdata.csv', 'a', newline='') as dont_touch:
    non_writer = csv.writer(dont_touch) #just open the file
with open('weatherdata.csv', 'r', newline='') as just_look:
    reader = csv.reader(just_look) #read file
    empty_test = [row for row in reader] #empty_test will = [] if empty
    if len(empty_test) == 0: #check if the array is empty
        opened = False #if array is empty, then file has never been opened
    else:
        opened = True #if array is not empty, then file has been opened
#write data to csv
with open('weatherdata.csv', 'a', newline='') as weatherfile:
    writer = csv.writer(weatherfile)
    sense.set_pixels(red_square)
    if opened == False: #if file has been opened don't write the header row again
        writer.writerow(['Date','Time','Temp(F)','Relative Humditity(%)','Pressure(mb)','CPU Utilization(%)','Response Time(sec)'])
    while(True):
        #gather time data
        now = datetime.now()
        current_date = now.strftime("%m/%d/%Y")
        current_time = now.strftime("%H:%M")

        #gather weather data & response time of sensor
        response_time_initial = datetime.now()
        tempinC = sense.get_temperature()
        tempinF = round((tempinC * 1.8) + 32,1)
        humidity = round(sense.get_humidity(),1)
        pressure = round(sense.get_pressure(),1)
        response_time_final = datetime.now()

        #gather CPU Data
        CPU = psutil.cpu_percent()
        response_time = response_time_final - response_time_initial

        #write data to csv 
        writer.writerow([current_date,current_time,tempinF,humidity,pressure,CPU,response_time.total_seconds()])
        weatherfile.flush()

        #wait for 20 mins to take data again
        print('wrote data at %s'%(current_time))
        sense.clear()
        sleep(1200)

        #end loop
        if(current_date == end_date):
            break


