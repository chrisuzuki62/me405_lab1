'''!
    @file encoder.py
    @brief A driver for reading from Quadrature Encoders
    @details This file creates an encoder calss that contains 3 methods that can
             be used in other files to get the change of the position of an
             encoder over time. It contains a construcotr method to instantiate each
             class object. A  get position method that returns the position of the encoder. 
             A zero poistion method that zeroes the position of the encoder to a specifed
             value. 
    @author Damond Li
    @author Chris Or
    @author Chris Suzuki
    @date 1/25/22
'''
import pyb
import time

class Encoder:
    '''!
        @brief Interface with quadrature encoders
        @details Creates a class that can be called into other python files that
                 is used to interface and read out the position of an encoder.
                 The class contains 3 methods. One to construct an encoder object,
                 one to get the position that the encoder reads, and one to set the 
                 position of the encoder to a specified value.
    '''

    def __init__(self, enc_num):
        
        '''!
            @brief Constructs an encoder object
            @details Instantiates an encoder object that contains 2 different
                     methods that can be used in other python files. This also
                     generally sets up the use of any encoder so multiple can 
                     be called in any file.
            @param enc_num Value used to establish each instance of the encoder.
                           Currently, this driver only supports up to 2 encoders.
                           Therefore this argument is either 1 or 2.
        '''
        ## Sets the maximum amount of ticks that the encoder can record. This
        ## is exactly the same as the maximum amount of bytes that the encoder
        ## can track since it is an 8 bit encoder.
        self.period = 65535
        
        ## Defines the two encoders that will be used and seperates usage
        if enc_num == 1:
            
            ## Sets the appropriate timer for encoder 1
            self.timer = pyb.Timer(4, prescaler = 0, period = self.period)
            
            ## Sets the appropriate pin 1 for encoder 1
            self.Pin1 = pyb.Pin(pyb.Pin.cpu.B6)
            ## Sets the appropriate pin 2 for encoder 1
            self.Pin2 = pyb.Pin(pyb.Pin.cpu.B7)
        
            ## Sets one channel that the encoder will use to track time
            self.ch1 = self.timer.channel(1,pyb.Timer.ENC_AB, pin=self.Pin1)
        
            ## Sets the second channel that the encoder will use to track time
            self.ch2 = self.timer.channel(2,pyb.Timer.ENC_AB, pin=self.Pin2)

        elif enc_num == 2:
            
            ## Sets the appropriate timer for encoder 2
            self.timer = pyb.Timer(8, prescaler = 0, period = self.period)
            
            ## Sets the appropriate pin 1 for encoder 2
            self.Pin1 = pyb.Pin(pyb.Pin.cpu.C6)
            ## Sets the appropriate pin 2 for encoder 2
            self.Pin2 = pyb.Pin(pyb.Pin.cpu.C7)
            
            ## Sets one channel that the encoder will use to track time
            self.ch1 = self.timer.channel(1,pyb.Timer.ENC_AB, pin=self.Pin1)
        
            ## Sets one channel that the encoder will use to track time
            self.ch2 = self.timer.channel(2,pyb.Timer.ENC_AB, pin=self.Pin2)
            
        ## Variable to represent the previous tick counter
        self.pos_1 = self.timer.counter()
        
        ## Variable to represent the current tick counter
        self.pos_2 = self.timer.counter()
        
        ## Variable to represent the current position
        self.current_pos = 0

    def read(self):
        '''!
            @brief Updates encoder position 
            @details Creates an update method that when ran will update the position
                     of the specfied encoder
            @return Returns the position of the encoder
        '''
        ## Defines the position of the encoder as the the timer linked to the encoder
        self.pos_1 = self.pos_2
        self.pos_2 = self.timer.counter()
        
        
        ## defines the delta as the difference between the encoder reading and the
        ## last recorded position of the encoder
        self.delta = self.pos_2 - self.pos_1
        
        if self.delta > 0 and self.delta > self.period/2:
            self.delta -= self.period
        if self.delta < 0 and abs(self.delta) > self.period/2:
            self.delta += self.period
        
        self.current_pos += self.delta
        
        return self.current_pos
    
    def zero(self):
        '''!
            @brief Zeros encoder position
            @details Creates a method that when called sets the position of the
                     encoder to zero.
        '''
        self.current_pos = 0


## main testing encoder code
if __name__ == '__main__':
    encoder1 = Encoder(1)
    encoder2 = Encoder(2)
    while(True):
        time.sleep(0.1)
        print([encoder1.read(), encoder2.read()])
        
