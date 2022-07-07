import time

# GPIOの初期設定
import RPi.GPIO as GPIO
GPIO.setMode(GPIO.BCM)

# GPIO04をPWM設定、周波数は50Hz
p = GPIO.PWM(4, 50)

# Dutiy Cycle 0％
p.start(0.0)

class MotorControl():
    def __init__(self, pin, frequency):
        # GPIO4(仮)を出力端子設定
        GPIO.setup(pin, GPIO.OUT)
        p = GPIO.PWM(pin,frequency)
    
    def rotate_motor(self,degree):
        
        