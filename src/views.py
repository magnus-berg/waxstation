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

from waxtimer import WaxTimer
import sf_14, sfb_20, sfb_24
import sfb_30, sfb_36

class BaseView:
    def update(buttons):
        if buttons[0] > 1 and buttons[3] > 1:
            return 4
        elif buttons[0] > 1:
            return 0
        elif buttons[1] > 1:
            return 1
        elif buttons[2] > 1:
            return 2
        elif buttons[3] > 1:
            return 3
            
class OffView(BaseView):
    def __init__(self, waxstation):
        self.display = waxstation.display
    
    def update(self, buttons):
        state = BaseView.update(buttons)
        
        self.display.clear()
        self.display.setFont(sfb_20)
        self.display.text("Off", 20, 20)
        self.display.show()
        return state

class FixedTempView(BaseView):
    def __init__(self, waxstation):
        self.display = waxstation.display
        self.settings = waxstation.settings
        self.goalTemp = waxstation.goalTemp()
        self.thermometer = waxstation.thermometer
        self.waxstation = waxstation
        
    def prepareUpdate(self, buttons):
        state = BaseView.update(buttons)
        self.display.clear()
        #self.display.setFont(sfb_24)
        self.display.setFont(sfb_30)
        txt = str(self.thermometer.calibratedTemp()) + "°"
        xpos = 64-int(self.display.size(txt)/2)
        self.display.text(txt, xpos, 15)

        self.display.setFont(sf_14)
        txt = str(self.goalTemp) + "°"
        xpos = 123-self.display.size(txt)
        self.display.text(txt, xpos, 0)
        if self.waxstation.power:
            self.display.image("heatingIcon", xpos-18, 1)
        return state
    
    def update(self, buttons):
        state = self.prepareUpdate(buttons)
        self.display.show()
        return state
        
        
class AutoView(FixedTempView):
    def __init__(self, waxstation):
        super().__init__(waxstation)
        self.timer = WaxTimer(self.settings.timer.value)
        self.hiTempReached = False

    def update(self, buttons):
        state = super().prepareUpdate(buttons)
        if self.hiTempReached == False:
            if self.waxstation.thermometer.calibratedTemp() >= self.waxstation.settings.hi.value:
                self.hiTempReached = True
                
            else:
                self.timer.reset()
            
        if self.timer.remaining() == 0:
            state = 1 # turn to low power
        self.display.setFont(sf_14)
        txt = "Heating..."
        if self.hiTempReached:
            txt = self.timer.minutes() + ":" + self.timer.seconds()
        
        self.display.text(txt, int(64-self.display.size(txt)/2), 45)
        self.display.show()
        return state