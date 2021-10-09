from machine import Pin, SoftI2C, I2C
from waxstation import WaxStation

from time import sleep_ms as sleep
#sda = Pin(26)
#scl = Pin(27)
offPin = Pin(10, Pin.IN, Pin.PULL_UP)
loPin = Pin(11, Pin.IN, Pin.PULL_UP)
hiPin = Pin(12, Pin.IN, Pin.PULL_UP)
autoPin = Pin(13, Pin.IN, Pin.PULL_UP)
relayPin = Pin(9, Pin.OUT)
dsPin = Pin(16)

i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
i2c2 = SoftI2C(sda=Pin(0), scl=Pin(1), freq=40000)
#i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=40000)

#from scanner import Scanner
#scanner = Scanner(i2c)
#scanner.scan()
#sleep(200)

from thermometer import Thermometer
#tempSensor = Thermometer(dsPin)
from thermometer import IR_Thermometer
tempSensor = IR_Thermometer(i2c2)


#import mlx90614
#_config1 = i2c.readfrom_mem(0x5a, 0x25, 2)

#temp = bytearray(2)
#temp[0] = MLX90614_TOBJ1
#temp[1]
#i2c.writeto(mlxAddr, temp)
#_config1 = i2c.readfrom_mem(0x5a, 0x25, 2)
#sensor = mlx90614.MLX90614(i2c)

#sleep(500)
#i2c.readfrom_mem(0x5a, 0x25, 2)
#i2c.readfrom_mem(0x5a, 0x05, 2)

waxStation = WaxStation({'offPin': offPin, 'loPin': loPin, 'hiPin': hiPin, 'autoPin': autoPin, 'i2c': i2c, 'relayPin': relayPin}, tempSensor)
waxStation.run()