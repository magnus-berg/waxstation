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

import sf_14, sf_18
import sfb_14, sfb_18, sfb_20
from time import sleep_ms as sleep
import usys
from display import Display
from settings import Settings
# Pages
# 0: Low temp
# 1: Hi temp
# 2: Timer
# 3: Calibration
# 4: Save
# 5: Factory reset
# 6: Halt
# 7: Exit

class SettingsView:
    def __init__(self, waxstation):
        self.page = 0
        self.display = waxstation.display
        self.settings = waxstation.settings
        self.__returnOnNextUpdate = False
        self.pages = [
            Page("Temperature", waxstation, [
                self.settings.hi,
                self.settings.lo,
            ], 0),
            Page("Temperature", waxstation, [
                self.settings.hi,
                self.settings.lo,
            ], 1),
            Page("Calibration", waxstation, [
                self.settings.calibrationHi,
                self.settings.calibrationLo,
            ], 0),            
            Page("Calibration", waxstation, [
                self.settings.calibrationHi,
                self.settings.calibrationLo,
            ], 1),
            Page("Timer", waxstation, [
                self.settings.timer
            ], 0),
            OptionsPage("Power Mode", waxstation, self.settings.powermode, Settings.powermodes()),
            ConfirmablePage("Factory Reset", waxstation, self.actionFactoryReset),
            ConfirmablePage("Halt", waxstation, self.actionHalt),
            ConfirmablePage("Save & exit", waxstation, self.actionSave),
            ConfirmablePage("Exit", waxstation, self.actionSave),
        ]
        
    def actionSave(self):
        self.settings.save()
        self.__returnOnNextUpdate = True
    def actionFactoryReset(self):
        self.settings.factoryReset()
        self.__returnOnNextUpdate = True
    def actionHalt(self):
        usys.exit()
        
    def update(self, buttons):
        if self.__returnOnNextUpdate:
            return 0
        
        pageChange = self.pages[self.page].update(buttons)
        if pageChange:
            self.page += pageChange
            self.page %= len(self.pages)

    def show(self, header, value):
        self.display.clear()
        self.display.setFont(sfb_14)
        self.display.text(header, 0, 0)
        if self.editMode:
            self.display.setFont(sfb_18)
        else:
            self.display.setFont(sf_18)
        self.display.text(str(value), 0, 30)
        self.display.show()

class Page:
    def __init__(self, title, waxstation, settings, index):
        self.waxstation = waxstation
        self.title = title
        self.settings = settings
        self.index = index
        self.editMode = False

    def printTitle(self):
        display = self.waxstation.display
        display.clear()
        display.setFont(sfb_14)
        display.text(self.title, 12, 0)
        
    def update(self, buttons):
        display = self.waxstation.display
        if self.editMode:
            if buttons[0] == 1 or buttons[0] > 10:
                self.settings[self.index].dec()
                sleep(75)
            if buttons[1] == 1 or buttons[1] > 10:
                self.settings[self.index].inc()
                sleep(75)
        elif buttons[0] == 1:
            return -1
        elif buttons[1] == 1:
            return 1
            
        if buttons[3] == 1:
            self.editMode ^= 1
            
        self.printTitle()
        
        for i, setting in enumerate(self.settings):
            if i == self.index:
                display.setFont(sfb_14)
                display.text(">", 2, 25+20*i)
            else:
                display.setFont(sf_14) 
            display.text(setting.name, 12, 25+20*i)

            if i != self.index or not self.editMode:
                display.setFont(sf_14) 
            display.text(str(setting.value), 45, 25+20*i)        
        display.show()
        
class ConfirmablePage(Page):
    def __init__(self, title, waxstation, action):
        super().__init__(waxstation, title, [], 0)
        self.title = title
        self.confirm = False
        self.waxstation = waxstation
        self.action = action
        
    def update(self, buttons):
        display = self.waxstation.display

        self.printTitle()
                
        if buttons[3] == 1:
            if self.confirm:
                self.action()
            self.confirm ^= 1
        elif buttons[0] == 1:
            return -1
        elif buttons[1] == 1:
            return 1

        if self.confirm:
            display.setFont(sfb_20)
            display.text("Confirm", 25, int(64-display.size("Confirm")/2))
        display.show()    

class OptionsPage(Page):
    def __init__(self, title, waxstation, setting, options):
        super().__init__(waxstation, title, [], 0)
        self.title = title
        self.waxstation = waxstation
        self.setting = setting
        self.options = options

    def update(self, buttons):
        display = self.waxstation.display

        if self.editMode:
            if buttons[0] == 1 or buttons[0] > 10:
                self.setting.dec()
                sleep(75)
            if buttons[1] == 1 or buttons[1] > 10:
                self.setting.inc()
                sleep(75)
        elif buttons[0] == 1:
            return -1
        elif buttons[1] == 1:
            return 1
            
        if buttons[3] == 1:
            self.editMode ^= 1


        self.printTitle()
        
        if self.editMode:
            display.setFont(sfb_14) 
        else:
            display.setFont(sf_14) 

        display.text(self.options[self.setting.value][0], 12, 25)
        display.show()