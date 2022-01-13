import pyb
import time

class Motor:
    '''! 
    This class implements a motor driver for an ME405 kit. 
    '''

    def __init__ (self, motor_num):
        '''! 
        Creates a motor driver by initializing GPIO
        pins and turning the motor off for safety. 
        @param en_pin (There will be several of these)
        '''
        print ('Creating a motor driver')
        if motor_num == 1:
            self.enable_pin = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
            self.Pin1 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
            self.Pin2 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
            self.timer = pyb.Timer (3, freq=20000)
            self.ch1 = self.timer.channel(1, pyb.Timer.PWM, pin=self.Pin1)
            self.ch2 = self.timer.channel(2, pyb.Timer.PWM, pin=self.Pin2)
            
        elif motor_num == 2:
            self.enable_pin = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
            self.Pin1 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
            self.Pin2 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
            self.timer = pyb.Timer (5, freq=20000)
            self.ch1 = self.timer.channel(1, pyb.Timer.PWM, pin=self.Pin1)
            self.ch2 = self.timer.channel(2, pyb.Timer.PWM, pin=self.Pin2)
            
    def enable(self):
        '''!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        '''
        self.enable_pin.high()
        
    def disable(self):
        '''!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        '''
        self.enable_pin.low()
        

    def set_duty_cycle (self, level):
        '''!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        '''
        print ('Setting duty cycle to ' + str (level))
        
        # Cap the duty cycle
        if level > 100:
            level = 100
        elif level < -100:
            level = -100
        
        if level > 0:
            self.ch1.pulse_width_percent (abs(level))
            self.ch2.pulse_width_percent (0)
        elif level < 0:
            self.ch1.pulse_width_percent (0)
            self.ch2.pulse_width_percent (abs(level))
        else:
            self.ch1.pulse_width_percent (0)
            self.ch2.pulse_width_percent (0)
        

if __name__ == '__main__':
    motor1 = Motor(1)
    motor2 = Motor(2)
    
    motor1.enable()
    motor2.enable()
    motor1.set_duty_cycle(50)
    motor2.set_duty_cycle(-100)
    
    time.sleep(3)
    
    motor1.disable()
    motor2.disable()
    