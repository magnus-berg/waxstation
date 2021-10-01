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

from math import floor
import time

class WaxTimer:
    def __init__(self, seconds):
        self.totalSeconds = seconds
        self.reset()

    def reset(self):    
        self.endTime = time.ticks_ms() + self.totalSeconds*1000
        
    def remaining(self):
        return max(0, self.endTime - time.ticks_ms())

    def seconds(self):
        s = floor(self.remaining()/1000) % 60
        return str(s) if s>9 else "0" + str(s)

    def minutes(self):
        m = floor(self.remaining()/60000)
        return str(m) if m>9 else "0" + str(m)

