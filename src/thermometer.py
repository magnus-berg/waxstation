"""
WAXstation - control software for a chain waxing machine
Copyright (C) 2021  Magnus Berg 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.    
"""

import time
import onewire, ds18x20
import mlx90614
import utime
        
class Thermometer:
    def __init__(self, dsPin):
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(dsPin))
        roms = self.ds_sensor.scan()
        self.rom = None
        if len(roms) > 0:
            self.rom = roms[0]
        self.temperature = -127
        try:
            self.ds_sensor.convert_temp()
        except:
            self.temperature = -127            
        self.lastCheck = time.ticks_ms()
        self.settings = None
        self.__initTemperature =  -127

    def read(self):
        if self.lastCheck + 750 < time.ticks_ms():
            try:
                self.temperature = self.ds_sensor.read_temp(self.rom)                
                self.ds_sensor.convert_temp()
                self.lastCheck = time.ticks_ms()
                if self.__initTemperature == -127:
                    self.__initTemperature == self.temperature
            except:
                self.temperature = -127                    
        
    def __calibrationValue(self):
        if self.temperature < self.settings.lo.value:
            difference = self.settings.lo.value - self.__initTemperature
            if difference == 0:
                return self.settings.lo.value
            else:
                k = self.settings.calibrationLo.value / difference
                return k * (self.temperature-self.__initTemperature)
        else:
            difference = self.settings.hi.value - self.settings.lo.value
            if difference == 0:
                return self.settings.lo.value
            else:
                k = (self.settings.calibrationHi.value-self.settings.calibrationLo.value) / difference
                return k * (self.temperature-self.settings.calibrationLo.value) + self.settings.calibrationLo.value
                
    def calibratedTemp(self):
        if self.__initTemperature == None:
            self.read()
            return -127
        if self.settings == None:
            return -127
        
        return int(self.temperature + self.__calibrationValue())
    
class IR_Thermometer(Thermometer):
    def __init__(self, i2c):
        self.sensor = mlx90614.MLX90614(i2c)
        self.temperature = -127
        self.lastCheck = time.ticks_ms()
        self.settings = None
        self.__initTemperature = None
        self.read()

    def read(self):
        self.temperature = int(self.sensor.object_temp)
        #self.temperature = int(self.sensor.ambient_temp)
        #print(self.temperature)
        if self.__initTemperature == None:
            self.__initTemperature = self.temperature
            