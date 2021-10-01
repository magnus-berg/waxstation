# waxstation

The purpose of this project is to make the process of waxing a bike chain a bit easier.

To get optimal results when waxing a bike chain you want a stable wax temperature. 
Optimal is 93 degrees celcius while waxing but before removing the chain 
from the pot it's preferable to lower the temperature to about 65 degrees.


The idea is to have a rice cooker as base and build an addon which includes 
a Raspberry Pi Pico, a temperature sensor and a relay to control the power of the rice cooker.
4 buttons will control the mode.
An 1.3 inch display shows current temperature, goal temperature and if the heater is activated.

The modes are:
- Off
- Low: Goal temperature is set to 65 degrees default
- High: Goal temperature is set to 93 degrees default
- Auto: As soon as the temperature will reach high, a timer, by default set to 30 minutes is started.
  When the timer ends the goal temperature will be set to low
- Settings: Customize all parameters



##Settings
You activate the settings by pressing button 1 and 4 simultaniously.
This will activate the settings view where you can edit the following:
- High and low temperature: can be set between 50 and 100 degrees
- Calibration at low and high temperature: calibrates the thermometer at 
  the two temperature levels. Value is an integer between -20 and 20.
- Timer: number of seconds for the auto-mode timer, can be set in steps of 10 between 10 and 3600.
- Power Mode: Since the rice cooker is consumes 500W the element gets to hot, to get a smother curve 
  the heater will be on a cycle when turned on. The first value is how long its on and the second is ho long it's off.
  Default is 5 / 5.


Parts
Rice cooker: Chapion CHRK210, any rice cooker would do the job but I choose this because it was cheap.
Raspberry Pi Pico
Mean Well RS-15-5 - Power supply
3vDC Relay for switching 10A 250VAC
1.3 inch oled display with SH1106-controller
4 momentary push buttons 


## Case
The case is 3D-printed and screwed together. The repo inlcudes both STL-files but also the source-files made with OpenSCAD.
