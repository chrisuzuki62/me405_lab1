"""! 
@file main.py
This file contains code which for Lab 0 which uses PWM to adjust
the brightness of an LED by making it increase from off to full
brightness in 5 second cycles.

@author Damond Li
@author Chris Or
@author Chris Suzuki
@date   6-Jan-2022 SPL Original file
"""

import pyb
import utime

def led_setup():
    """!
    @brief   Sets up the LED and timer
    @details This method initiates pins on the nucleo board PA0
             as and LED output and assigns the frequency and timer
             channel for it.
    """
    pA0 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    tim2 = pyb.Timer(2, freq = 20000)
    global ch2
    ch2 = tim2.channel(1, pyb.Timer.PWM_INVERTED, pin=pA0)

def led_brightness(x):
    """!
    @brief   Sets brightness of the LED and limits value
    @details This method takes in a value for brightness
             and changes the brightness of the LED based
             on the value.
    @param   x Sets the percent brightness of the LED
    """
    if x>100:
        x = 100
    elif x<0:
        x = 0
    ch2.pulse_width_percent(x)

if __name__ == "__main__":
    led_setup()
    startTime = 0
    relativeTime = 0
    currentTime = 0
    while (True):
        try:
            currentTime = utime.ticks_ms()
            relativeTime = utime.ticks_diff(currentTime, startTime)
            relativeTime %= 5000
            led_brightness((relativeTime/5000)*100)
        
        except KeyboardInterrupt:
            break
    
print('Program Terminated')