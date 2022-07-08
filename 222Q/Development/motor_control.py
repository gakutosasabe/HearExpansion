import time

# GPIOの初期設定
import RPi.GPIO as GPIO

class SG92R_Control():
    def __init__(self, pin):
        # GPIO4(仮)を出力端子設定
        self.mpin = pin
        GPIO.setup(self.mPin, GPIO.OUT)
        self.mPwm = GPIO.PWM(self.mPin,50)
    
    def SetPos(self,pos): #位置セット
        #Duty ratio = 2.5 ~ 12.0% : 0.5ms~2.4ms : 0~ 180deg
        duty = (12-2.5)/180*pos + 2.5 
        self.mPwm.start(duty)

    def Cleanup(self): #0degにして終了
        self.SetPos(90)
        time.sleep(1)
        GPIO.setup(self.mPin, GPIO.IN)
        