import time
import Adafruit_BBIO.GPIO as GPIO
import os

import Adafruit_BBIO
import board

import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd


i2c = busio.I2C(board.SCL, board.SDA)
cols = 20
rows = 4
lcd = character_lcd.Character_LCD_I2C(i2c, cols, rows)

GPIO.setup("P2_4", GPIO.IN)
GPIO.setup("P2_6", GPIO.IN)        

t_1 = 0.0
t_2 = 0.0
d = 17.75
sensor_1 = False

try:
    lcd.message = ("Ready")
    os.system("aplay /var/lib/cloud9/Ready2.wav")
    while True:
        # if GPIO.input("P2_4") == 0:
        #     print("P2_4 = 0")
        #     t_1 = 0
        # if GPIO.input("P2_6") == 0:
        #     print("P2_6 = 0")
        #     t_2 = 0
        if sensor_1 and (time.time() - t_1 > 2.0):
            print("Reset P2_4")
            sensor_1 = False
            t_1      = 0
        if GPIO.input("P2_4") == 1 and not sensor_1:
            print("P2_4 = 1")
            sensor_1 = True
            t_1 = time.time()
            # print("motion1 = {}".format(t_1))
        # time.sleep(0.1)
        if GPIO.input("P2_6") == 1 and sensor_1:
            print("P2_6 = 1")
            t_2 = time.time()
            t = t_2-t_1
            s = d/t
            # s = round(s, 4)
            lcd.message = ("speed = {0:3.7}".format(s))
            if s < 40:
                os.system("aplay /var/lib/cloud9/Too_Slow.wav")
            if (s >= 40) and (s <= 60):
                os.system("aplay /var/lib/cloud9/perf_putt.wav")
            if s > 60:
                os.system("aplay /var/lib/cloud9/Too_Fast.wav")
            time.sleep(2)
            lcd.clear()
            lcd.message = ("Ready")
            os.system("aplay /var/lib/cloud9/Ready2.wav")
            sensor_1 = False
        time.sleep(0.038) # based on sensor timing
        #print("speed = {}".format(distance // (t_2 - t_1))
        
        # s = float((distance)/t)

        
        
        # speed = float((distance // (t_2 - t_1)) #calculate speed
        # print("speed = {}".format(speed))
except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program Complete")
