import motor
import encoder
import time

start_time = time.time()
encoder1 = encoder.Encoder(1)
encoder2 = encoder.Encoder(2)

motor1 = motor.Motor(1)
motor2 = motor.Motor(2)

motor1.enable()
motor2.enable()

motor1.set_duty_cycle(100)
motor2.set_duty_cycle(-100)

while (time.time() - start_time < 5):
    print([encoder1.read(), encoder2.read()])
          
motor1.disable()
motor2.disable()