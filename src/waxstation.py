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

from machine import Pin
from settings import Settings
from display import Display
import time
from time import sleep_ms as sleep
import time
from thermometer import Thermometer
from views import OffView, FixedTempView, AutoView
from settingsview import SettingsView

# WaxStation has 4 states
# 0 - Off
# 1 - Low temp
# 2 - High temp
# 3 - Auto temp
# 4 - Settings
class WaxStation:
    def __init__(self, pins, thermometer):
        self.settings = Settings()
        self.settings.load()
        self.waxtimer = None
        self.state = -1
        self.pins = pins
        self.offPin = pins['offPin']
        self.loPin = pins['loPin']
        self.hiPin = pins['hiPin']
        self.autoPin = pins['autoPin']
        self.i2c = pins['i2c']
        self.relayPin = pins['relayPin']
        self.input = Input([self.autoPin, self.hiPin, self.loPin, self.offPin])
        self.display = Display(self.i2c)
        self.view = OffView(self)
        self.thermometer = thermometer
        self.power = 0
        self.thermometer.settings = self.settings
        self.__powerTime = time.ticks_ms()
        self.powerled = Pin(25, Pin.OUT)
        self.screenTimer = -1
        

    def updatePower(self):
        timePassed = int((time.ticks_ms() - self.__powerTime)/1000)
        pm = self.settings.currentPowerMode()
        if  timePassed > (pm[1] + pm[2]):
            self.__powerTime = time.ticks_ms()
        elif timePassed > pm[1]:
            self.relayPin.value(0)
            self.powerled.value(0)
        else:
            self.relayPin.value(self.power)
            self.powerled.value(self.power)
            
    def run(self):
        while self.state >= -1:
            if self.screenTimer != 0 and self.screenTimer < time.ticks_ms() :
                self.display.poweroff()
                self.screenTimer = 0
                
            self.thermometer.read()
            
            if self.thermometer.temperature != -127 and self.thermometer.calibratedTemp() < self.goalTemp():
                self.power = 1
            elif self.thermometer.temperature == -127 or self.thermometer.calibratedTemp() >= self.goalTemp():
                self.power = 0
    
            self.updatePower()
            self.relayPin.value(self.power)
            
            buttons = self.input.update()
            newState = self.view.update(buttons)
            if newState != None and newState != self.state:
                self.state = newState
                self.display.poweron()
                if self.state == 0:
                    self.view = OffView(self)
                    self.view.update(buttons)
                    self.relayPin.value(0)
                    self.screenTimer = time.ticks_ms() + 3000
                elif self.state == 1 or self.state == 2:
                    self.view = FixedTempView(self)
                elif self.state == 3:
                    self.view = AutoView(self)
                elif self.state == 4:
                    self.view = SettingsView(self)

                if self.state != 0:
                    self.screenTimer = 0
        if self.state == -99:
            return self.state
            
    def goalTemp(self):
        if self.state == 1:
            return self.settings.lo.value
        elif self.state == 2: 
            return self.settings.hi.value
        elif self.state == 3: ## ???
            return self.settings.hi.value
        else:
            return 0

        

    
class Input:
    def __init__(self, pins):
        self.pins = pins
        self.state = [0] *len(self.pins)
        self.returnValue = [0] *len(self.pins)

    def update(self):
        for index, pin in enumerate(self.pins):
            pinValue = 1 if pin.value() == 0 else 0
            if pinValue == 1:
                self.returnValue[index] += 1
            else:
                self.returnValue[index] = 0
            self.state[index] = pinValue
            
        return self.returnValue        



