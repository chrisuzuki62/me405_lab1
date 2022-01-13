'''! @file encoder.py
    @brief A driver for reading from Quadrature Encoders
    @details This file creates an encoder calss that contains 5 methods that can
             be used in other files to get the change of the position of an
             encoder over time. It contains a construcotr method to instantiate each
             class object. An update method to update the position that the encoder
             reads. A  get position method that returns the position of the encoder. 
             A set poistion method that sets the position of the encoder to a specifed
             value. And a get delta function that returns the change in position of the
             encoder over time.
    @author Chris Suzuki
    @date 10/21/21
'''
import pyb

class encoder:
    ''' @brief Interface with quadrature encoders
        @details Creates a class that can be called into other python files that
                 is used to interface and read out the position of an encoder.
                 The class contains 5 methods. One to construct an encoder object,
                 one to update the position that the encoder reads, one to get the
                 position that the encoder reads, one to set the position of the
                 encoder to a specified value, and one to return the change of
                 position of the encoder over time.
    '''

    def __init__(self, enc_num):
        
        ''' @brief Constructs an encoder object
            @details Instantiates an encoder object that contains 4 different
                     methods that can be used in other python files. this also
                     generally sets up the use of any encoder so multiple can 
                     be called in any file.
            @ param PinA Inputs a pin letter and number
            @ param PinA Inputs a pin letter and number
            @ param tim_num Inputs the number of the timer that will be used
        '''
        ## Sets the maximum amount of ticks that the encoder can record. This
        #  is exactly the same as the maximum amount of bytes that the encoder
        #  can track since it is an 8 bit encoder.
        self.period = 65535
        
        ## Defines the timer that the encoder will use
        if enc_num == 1:
            self.timer = pyb.Timer(3, prescaler = 0, period = self.period)
        
            self.Pin1 = pyb.Pin(pyb.Pin.cpu.B6)
            self.Pin2 = pyb.Pin(pyb.Pin.cpu.B7)
        
            ## Sets one channel that the encoder will use to track time
            self.ch1 = self.timer.channel(1,pyb.Timer.ENC_AB, pin=self.Pin1)
        
            ## Sets one channel that the encoder will use to track time
            self.ch2 = self.timer.channel(2,pyb.Timer.ENC_AB, pin=self.Pin2)

        elif enc_num == 2:
            self.timer = pyb.Timer(5, prescaler = 0, period = self.period)
            
            self.Pin1 = pyb.Pin(pyb.Pin.cpu.C6)
            self.Pin2 = pyb.Pin(pyb.Pin.cpu.C7)
            
            ## Sets one channel that the encoder will use to track time
            self.ch1 = self.timer.channel(1,pyb.Timer.ENC_AB, pin=self.Pin1)
        
            ## Sets one channel that the encoder will use to track time
            self.ch2 = self.timer.channel(2,pyb.Timer.ENC_AB, pin=self.Pin2)
            
            
        ## sets the a reference to the amount of ticks that the encoder has recorded
        self.ref_count = 0
        
        ## Sets the inital position of the encoder to 0
        self.current_pos = 0

    def read(self):
        ''' @brief Updates encoder position and delta
            @details Creates an update method that when ran will update the position
                     and the delta of the specfied encoder
            @return returns the position and delta of the encoder
        '''
        ## Defines the position of the encoder as the the timer linked to the encoder
        self.encoder_1 = self.timer.counter()
        
        ## defines the delta as the difference between the encoder reading and the
        #  reference count
        self.delta = self.encoder_1 - self.ref_count
        
        if self.delta > 0 and self.delta > self.period/2:
            self.delta -= self.period
        if self.delta < 0 and abs(self.delta) > self.period/2:
            self.delta += self.period
         
        self.ref_count = self.encoder_1
        self.current_pos += self.delta
        
        return self.current_pos
    
    def zero(self, position):
        ''' @brief Sets encoder position
            @details Creates a method that when called sets the position of the
                     encoder to a specified input value to the code.
            @param position The new position of the encoder shaft
        '''
        self.current_pos = position


if __name__ == '__main__':
    while(True):
        encoder1 = encoder.encoder(1)
        encoder1.read()
        
