"""
--------------------------------------------------------------------------
Putt Project
--------------------------------------------------------------------------
License:   
Copyright 2018-2020 Grace Wilson

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""

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

GPIO.setup("P2_4", GPIO.IN) # sensor 1
GPIO.setup("P2_6", GPIO.IN) # sensor 2
GPIO.setup("P2_2", GPIO.IN) # record button
GPIO.setup("P2_8", GPIO.IN) # history button
GPIO.setup("P2_10", GPIO.IN) # gpio52 toggle1 button
GPIO.setup("P2_19", GPIO.IN) # gpio 27 toggle2 button

t_1 = 0.0
t_2 = 0.0
d = 17.75
reading = []
index = 0

def record():
    sensor_1 = False
    lcd.clear()
    lcd.message = ("Ready")
    os.system("aplay /var/lib/cloud9/Ready2.wav")
    while True:
        if sensor_1 and (time.time() - t_1 > 2.0):
            print("Reset P2_4")
            sensor_1 = False
            t_1      = 0
        if GPIO.input("P2_4") == 1 and not sensor_1:
            print("P2_4 = 1")
            sensor_1 = True
            t_1      = time.time()
        if GPIO.input("P2_6") == 1 and sensor_1:
            print("P2_6 = 1")
            t_2      = time.time()
            t        = t_2-t_1
            s        = d/t
            s = round(s, 5)
            reading.append(s)
            # s = round(s, 4)
            lcd.message = ("speed = {0:3.7}".format(s))
            if s < 60:
                os.system("aplay /var/lib/cloud9/Too_Slow.wav")
            if (s >= 60) and (s <= 80):
                os.system("aplay /var/lib/cloud9/perf_putt.wav")
            if s > 80:
                os.system("aplay /var/lib/cloud9/Too_Fast.wav")
            time.sleep(0.75)
            lcd.clear()
            lcd.message = ("Ready")
            os.system("aplay /var/lib/cloud9/Ready2.wav")
            sensor_1 = False
        if GPIO.input("P2_8") == 0:
            break
        time.sleep(0.038) # based on sensor timing


def print_history(index):
    message = ""
    
    for i, item in enumerate(reading):
        if (i >= index) and (i < index + 4):
            message = message + "{0}: {1}\n".format(i + 1, item)
            
    lcd.message = message

    
def history():
    print("History")
    index = 0
    print_history(index)
    os.system("aplay /var/lib/cloud9/History.wav")

    while True:
        if GPIO.input("P2_10") == 0 and index > 0:
            index = index - 1
            print_history(index)
        if GPIO.input("P2_19") == 0 and index < len(reading) - 1:
            index = index + 1
            print_history(index)
        if GPIO.input("P2_2"):
            break;
        time.sleep(0.1)

"""
    if GPIO.input("P2_10") == 1:
        pass
    if GPIO.input("P2_19") == 1:
        pass
    if GPIO.input("P2_10") == 0:
         if index > 0:
            index = index - 1
    if GPIO.input("P2_19") == 0:
         if index < len(reading) - 1:
            index = index + 1
"""    
try:
    while True:
        if GPIO.input("P2_2") == 1:
            pass
        time.sleep(0.1)
        if GPIO.input("P2_8") == 1:
            pass
        time.sleep(0.1)
        if GPIO.input("P2_2") == 0:
            print("record")
            record()
        time.sleep(0.1)
        if GPIO.input("P2_8") == 0:
            print("history")
            history()
        time.sleep(0.1)
        # speed = float((distance // (t_2 - t_1)) #calculate speed
        # print("speed = {}".format(speed))
        
except KeyboardInterrupt:
    GPIO.cleanup()
    lcd.clear()
    print("Program Complete")