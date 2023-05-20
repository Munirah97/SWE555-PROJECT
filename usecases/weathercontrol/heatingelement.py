#|               Component: Heat Element                         |
#| manipulate Temeprature by 1C per hour based on visitors count |                     
#|               Author: Hadi Almansour                          |

from time import *
from physical import *
from gpio import *
from environment import Environment

# rate of change of environment variables
HUMIDITY_RATE = -2./3600; # -2% per hour
TEMPERATURE_RATE = 1./3600; # 1C per hour
VOLUME_AT_RATE = 100000.
MAX_RATE = 1.e6

input = 0.

def setup ():
	
    add_event_detect(0, isr) # introducing an interrupt
    isr()
# the function that detects changes in the pins connected to the heating element 
def isr ():
    global input
    input1 = customRead(0)
    print("Recieved Value = {} ".format(input1))
    input = int(input1)
    print("input = {}".format(input))
    if  input > 0 :
        digitalWrite(5, HIGH) # On State Logo 
    else:
        digitalWrite(5, LOW) # Off state logo

# main loop
def loop ():
    updateEnvironment()#updates environment
    delay(1000)

#updates environment
def updateEnvironment ():
    humidity_rate = input*HUMIDITY_RATE*VOLUME_AT_RATE / Environment.getVolume() # humdity rate function
    temperature_rate = input*TEMPERATURE_RATE*VOLUME_AT_RATE / Environment.getVolume() # Temperature rate function                                                                                                                                                          
    Environment.setContribution("Humidity", humidity_rate, MAX_RATE, True) # changes humidity
    Environment.setContribution("Ambient Temperature", temperature_rate, MAX_RATE, True) # changes temperature


if __name__ == "__main__":
    setup()
    while True:
        loop()
        sleep(0)
        

