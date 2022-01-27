"""!
@file       motor.py
@brief      A driver for the motors in ME405 kit
@details    This file contains code which for the Lab 1 motor driver. This motor driver is 
            responsible for interfacing with the motor. This driver creates the motor 
            objects that will be used in the motor task.

@author Damond Li
@author Chris Or
@author Chris Suzuki
@date   27-Jan-2022 SPL Original file
"""

import pyb
import time

class Motor:
    '''! 
    @brief      Interface with ME405 motors
    @details    Creates a class that can be called into other python files 
                that is used to interface and set the duty cycle of a motor.
                The class contains methods to enable and disable the motors and
                to set the duty cycle.  
    '''

    def __init__ (self, motor_num):
        '''! 
        @brief      Constructs a motor object
        @details    Creates a motor driver by initializing GPIO pins and 
                    turning the motor off initially for safety. This also sets 
                    up the pin objects for motors 1 and 2 for use in other 
                    files.
        @param enable_pin Enable pin sets the pin corresponding to each motor 
                          to be set to the output mode. (There will be several 
                          of these)
        '''
        print ('Creating a motor driver')
        if motor_num == 1:
            ## Object that enables Pin A10 for Motor 1 by the output mode.
            self.enable_pin = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
            ## Object for Motor 1, Pin 1 as Pin B4
            self.Pin1 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
            ## Object for Motor 1, Pin 2 as Pin B5
            self.Pin2 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
            ## Object to set the timer and its frequency for Motor 1
            self.timer = pyb.Timer (3, freq=20000)
            ## Object for Motor 1, channel 1 corresponding to Pin 1
            self.ch1 = self.timer.channel(1, pyb.Timer.PWM, pin=self.Pin1)
            ## Object for Motor 1, channel 2 corresponding to Pin 2
            self.ch2 = self.timer.channel(2, pyb.Timer.PWM, pin=self.Pin2)
            
        elif motor_num == 2:
            ## Object that enables Pin C1 for Motor 2 by the output mode.
            self.enable_pin = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
            ## Object for Motor 2, Pin 1 as Pin A0
            self.Pin1 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
            ## Object for Motor 2, Pin 2 as Pin A1
            self.Pin2 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
            ## Object to set the timer and its frequency for Motor 2
            self.timer = pyb.Timer (5, freq=20000)
            ## Object for Motor 2, channel 1 corresponding to Pin 1
            self.ch1 = self.timer.channel(1, pyb.Timer.PWM, pin=self.Pin1)
            ## Object for Motor 2, channel 2 corresponding to Pin 1
            self.ch2 = self.timer.channel(2, pyb.Timer.PWM, pin=self.Pin2)
            
    def enable(self):
        """! 
        @brief      Enables motor 
        @details    This method enables the motor by setting the pin to high
        """
        self.enable_pin.high()
        
    def disable(self):
        """!
        @brief      Enables motor 
        @details    This method disables the motor by setting the pin to low
        """
        self.enable_pin.low()

    def set_duty_cycle (self, level):
        '''!
        @brief      Sets the motor duty cycle
        @detials    This method sets the duty cycle to be sent
                    to the motor to the given level. Positive values
                    cause torque in one direction, negative values
                    in the opposite direction.
        @param level A signed integer holding the duty
                     cycle of the voltage sent to the motor 
        '''
        print ('Setting duty cycle to ' + str (level))
        
        ## Limits the duty cycle to +/- 100%
        if level > 100:
            level = 100
        elif level < -100:
            level = -100
        
        ## Sets PWM value to channels 1 or 2 depending on positive or negative 
        ## which determines direction. The value of level is set as a positive
        ## input value through the use of abs. 
        if level > 0:
            self.ch1.pulse_width_percent (abs(level))
            self.ch2.pulse_width_percent (0)
        elif level < 0:
            self.ch1.pulse_width_percent (0)
            self.ch2.pulse_width_percent (abs(level))
        else:
            self.ch1.pulse_width_percent (0)
            self.ch2.pulse_width_percent (0)

## The following code only runs if this file is run as the main script;
## it does not run if this file is imported as a module. Tests motor driver.
if __name__ == '__main__':
   
    # Object for Motor 1
    motor1 = Motor(1)
    # Object for Motor 2
    motor2 = Motor(2)
    
    # Calling Motor 1 enable method to enable Motor 1
    motor1.enable()
    # Calling Motor 2 enable method to enable Motor 2
    motor2.enable()
    
    # Manual input of Motor 1 duty cycle
    motor1.set_duty_cycle(50)
    # Manual input of Motor 2 duty cycle
    motor2.set_duty_cycle(-100)
    
    # Set the amount of time for motors to run [s]
    time.sleep(3)
    
    # Calling Motor 1 disable method to disable Motor 1
    motor1.disable()
    # Calling Motor 2 disable method to disable Motor 2
    motor2.disable()
    