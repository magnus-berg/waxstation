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

import json
class Setting:
    def __init__(self, name, value, limits, increment = 1):
        self.name = name
        self.value = value
        self.limits = limits
        self.increment = increment
        
    def inc(self):
        if (self.value + self.increment) in self.limits:
            self.value += self.increment
            
    def dec(self):
        if (self.value - self.increment) in self.limits:
            self.value -= self.increment
            
class Settings:
    __settingsFile = "settings.txt"

    def __init__(self):
        self.__setDefaultValues()
        
    def load(self):
        try:
            f = open(self.__settingsFile)
            s = json.loads(f.read())
            self.hi.value = s['hiValue']
            self.lo.value = s['loValue']
            self.timer.value = s['timer']
            self.calibrationLo.value = s['calibrationLo']
            self.calibrationHi.value = s['calibrationHi']
            self.powermode.value = s['powermode']
            f.close()
            print(s)
        except:
            print("Failed to open settings")
            self.save()

    def save(self):
        f = open(self.__settingsFile, "w")
        f.write(self.export())
        f.close()

        
    def export(self):
        return json.dumps({
            'hiValue': self.hi.value,
            'loValue': self.lo.value,
            'timer': self.timer.value,
            'calibrationLo': self.calibrationLo.value,
            'calibrationHi': self.calibrationHi.value,
            'powermode': self.powermode.value,
            })

    def __setDefaultValues(self):
        self.hi = Setting("Hi", 93, range(50, 100))
        self.lo = Setting("Lo", 64, range(50, 100))
        self.calibrationHi = Setting("Hi", 0, range(-20, 20))
        self.calibrationLo = Setting("Lo", 0, range(-20, 20))
        self.timer = Setting("Sec", 1800, range(10, 3600), 10)
        self.powermode = Setting("Power Mode", 0, range(0, len(Settings.powermodes())))

    def factoryReset(self):
        self.__setDefaultValues()
        self.save()

    def currentPowerMode(self):
        ps = Settings.powermodes()
        return ps[self.powermode.value]
    
    def powermodes():
        return [
            ('5 / 5', 5, 5),
            ('10 / 10', 10, 10),
            ('20 / 20', 20, 20),
            ('5 / 10', 5, 10),
            ('10 / 20', 10, 20),
            ('10 / 5', 10, 5),
            ('20 / 10', 20, 10),
            ('1 / 0', 1, 0),
            ]