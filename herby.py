import time
from mraa import getGpioLookup
from upm import pyupm_buzzer as upmBuzzer
import pandas as pd
import datetime

#Moisture and buzzer
from grove.grove_moisture_sensor import GroveMoistureSensor
from grove.display.jhd1802 import JHD1802

#TDS
from TDS import GroveTDS

#Light sensor
from grove.grove_light_sensor_v1_2 import GroveLightSensor

#humidity and temperature
from seeed_dht import DHT

#import fuer csv Datei
import csv

#main function
        

def moisture_tds_main():

        lcd = JHD1802()
        
        sensor = GroveMoistureSensor(4)
        
        #buzzer = upmBuzzer.Buzzer(getGpioLookup('GPIO12'))
        sensor_tds = GroveTDS(0)
        print('TDS Value: {0}'.format(sensor_tds.TDS))
        
        mois = sensor.moisture
        if 0 <= mois and mois < 300:
            level = 'dry'
            #buzzer.playSound(upmBuzzer.BUZZER_DO, 200000)
        elif 300 <= mois and mois < 600:
            level = 'moist'
        else:
            level = 'wet'
        
                
        print('moisture: {}, {}'.format(mois, level))
            
        lcd.setCursor(0, 0)
        lcd.write('moisture: {0:>6}'.format(level))
            
        lcd.setCursor(1,0)
        lcd.write('TDS: {0:>12}'.format(sensor_tds.TDS)) #hier muss noch ein threshold hin
        
        return level,sensor_tds.TDS
        
        
def Light_main():           
        sensor = GroveLightSensor(2)
        print('light value {}'.format(sensor.light))
        
        return sensor.light
        

def temp_hum_main():
        lcd = JHD1802()
        
        sensor = DHT('11', 5)
        

        humi, temp = sensor.read()
        print('temperature {}C, humidity {}%'.format(temp,humi))
                
        lcd.setCursor(0,0)
        lcd.write('temperature: {0:2}C'.format(temp))

        lcd.setCursor(1,0)
        lcd.write('humidity: {0:5}%'.format(humi))
        
        return humi,temp
        

def main():
    
    
    while True:

        mois,tds = moisture_tds_main()
        time.sleep(2)
        light = Light_main()
        hum,temp = temp_hum_main()
        time.sleep(5)
        
        today = pd.to_datetime('today')
        toWrite = [tds, mois, light, temp, hum]
        
        df = pd.read_csv('test.csv')
        df[today] = toWrite
        df.to_csv('test.csv', index=False)

        

if __name__ == '__main__':
    main()
