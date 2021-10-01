from machine import Pin, I2C
from waxstation import WaxStation

sda = Pin(26)
scl = Pin(27)
offPin = Pin(10, Pin.IN, Pin.PULL_UP)
loPin = Pin(11, Pin.IN, Pin.PULL_UP)
hiPin = Pin(12, Pin.IN, Pin.PULL_UP)
autoPin = Pin(13, Pin.IN, Pin.PULL_UP)
relayPin = Pin(9, Pin.OUT)
dsPin = Pin(16)

#temp_i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)


from thermometer import Thermometer
ds18b20 = Thermometer(dsPin)
#tempSensor = IR_Thermometer(temp_i2c)

waxStation = WaxStation({'offPin': offPin, 'loPin': loPin, 'hiPin': hiPin, 'autoPin': autoPin, 'sdaPin': sda, 'sclPin': scl, 'relayPin': relayPin}, ds18b20)
waxStation.run()