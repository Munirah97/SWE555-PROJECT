#|               Usecase: Weather Quality            |
#| To Control Temperature where visitors are located |                     
#|               Author: Hadi Almansour              |
from gpio import *
from time import *

def main():
	# Zero State Variables Initialization 
	entryCount = 0 # Visitor Counter inside the building
	previousEntryState = 0#perserve the previous state of entry sensor
	previousExitState= 0 #perserve the previous state of exit sensor
	lcdString = "Visitor Counter = {}\n Temperature: {}".format(0,0) # LCD main inteface screen
	
	# Pins initialization 
	lcdScreen = 0 #LCD Screen Pin
	entrySensor = 1 # Entry Sensor
	exitSensor = 4 # Exit Sensor
	visitorReplicationElement = 2 # Heat Element Pin which  Replicatees the Viistors
	airConditioner = 3 # AC pins
	temperatureSensor = A0 # Temperature Sensor Pin
	
	# INPUT/OUTPUT Component states
	pinMode(lcdScreen, OUT)
	pinMode(entrySensor, IN) 
	pinMode(visitorReplicationElement, OUT)
	pinMode(exitSensor, IN) 
	pinMode(temperatureSensor, IN)
	pinMode(airConditioner, OUT)
	customWrite(lcdScreen, "Initialization Compelete") # intialize message of LCD
	
	#The infinte loop()
	while True:
		
		# Temperature Monitoring and Controlling
		temperatureReading = 200./1023 * analogRead(temperatureSensor) - 100 # Transfer Function of Temperature Sensor
		lcdString = lcd_String(entryCount, temperatureReading) #Creates a String that's updated with the new Visitor Count and Temperature reading
		customWrite(lcdScreen, lcdString) #updates LCD screen 
		
		# Temperature monitoring
		if temperatureReading > 25:	
			digitalWrite(airConditioner, HIGH) # Turn on AC if Temperature > 25
		else:
			digitalWrite(airConditioner, LOW) # Turn off Temperature <= 25
			
		# Incrementing Entry Sensor Counting
		entryState = digitalRead(1)  # Reads the state of entry sensor
		if (entryState == HIGH and previousEntryState == 0): # Check for a change in state of the sensor
			entryCount = entryCount + 1 # it will incerement 
			previousEntryState = 1 # it will save previous state
			entryCountStr = str(entryCount) # Prepares a string to be used by CustomWrite 
			customWrite(2, entryCountStr) # Changes Temperature based on the number of people
			print("Entry_Count: {}".format(entryCount)) # this is for debugging only
			lcdString = lcd_String(entryCount, temperatureReading) #Creates a String that's updated with the new Visitor Count and Temperature reading
			customWrite(lcdScreen, lcdString) #updates LCD screen 
		elif (entryState == HIGH and previousEntryState == 1): # checks if no changes occurs in the sensor
			previousEntryState = 1 # keep the state as it is as the state did not chage
			print("Entry_Count: {}".format(entryCount))
		else: #default case
			previousEntryState = 0
			
		# Deceremting Exit Sensor Counter 
		exitState = digitalRead(exitSensor)
		if (exitState == HIGH and previousExitState == 0):
			entryCount = entryCount - 1 # it will decerement 
			previousExitState = 1 # it will save previous state
			entryCountStr = str(entryCount) # Prepares a string to be used by CustomWrite 
			customWrite(2, entryCountStr) # Changes Temperature based on the number of people
			print("Entry_Count: {}".format(entryCount)) # this is for debugging only
			lcdString = lcd_String(entryCount, temperatureReading)#Creates a String that's updated with the new Visitor Count and Temperature reading
			customWrite(lcdScreen, lcdString)  #updates LCD screen 
		elif (exitState == HIGH and previousExitState == 1):
			previousStateExit = 1 # keep the state as it is as the state did not chage
			print("Entry_Count: {}".format(entryCount))
		else:
			previousExitState = 0
			
		# Keeps only positive counting values
		if entryCount < 0: 
			entryCount = 0
		delay(50) # delays 50ms between each reading

# Function that prints into the LCD screen		
def lcd_String(entryCount, temperatureReading):
	lcdString = "Visitor = {}\n Temp: {}".format(entryCount,temperatureReading)
	return lcdString

if __name__ == "__main__":
	main()
