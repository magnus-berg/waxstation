# WAXstation

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
- Low: Goal temperature is set to 65 degrees default.
- High: Goal temperature is set to 93 degrees default.
- Auto: As soon as the temperature will reach high, a timer, by default set to 30 minutes is started.
  When the timer ends the goal temperature will be set to low.
- Settings: Customize all parameters.


### Settings
You activate the settings by pressing button 1 and 4 simultaniously.
This will activate the settings view where you can edit the following:
- High and low temperature: can be set between 50 and 100 degrees
- Calibration at low and high temperature: calibrates the thermometer at 
  the two temperature levels. Value is an integer between -20 and 20.
- Timer: number of seconds for the auto-mode timer, can be set in steps of 10 between 10 and 3600.
- Power Mode: Since the rice cooker consumes 500W the element gets to hot. To get a smother curve 
  the heater will be on a cycle when temperature is to low. The first value is how many seconds it will be turned on and the second is how many seconds it is turned off.
  Default is 5 / 5, so it will switch every 5 second.

There is support for both Dallas DS18b20/DS18b20+ and IR Temperature Sensor Module with MLX90614-sensor. I was not able to get accurate temperature 
readings without putting the sensor in the bowl so to be able to go with an integrated sollution I tried an IR sollution. The DS18b20 uses OneWire for communication 
while the MLX90614 uses I2C and there fore can be on the same buis as the display.

Parts
- Rice cooker: Chapion CHRK210, any rice cooker with a capacity between 1 and 1.5 litres would do the job but I choose 
  this because it was cheap and the shape is like a cylinder which makes it easy to create a case for the electronics.
- Raspberry Pi Pico
- Mean Well RS-15-5 - Power supply [DigiKey](https://www.digikey.se/product-detail/sv/mean-well-usa-inc/RS-15-5/1866-4133-ND/7706168)
- 3vDC Relay for switching 10A 250VAC [amazon.com](https://www.amazon.com/3V-Relay-Module-Optocoupler-Development/dp/B01M0E6SQM/ref=sr_1_1_sspa?crid=1S9NN9JLTOM72&dchild=1&keywords=3v+relay&qid=1633087068&sprefix=3v+rela%2Caps%2C230&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFOUUswQzJVWVJERk4mZW5jcnlwdGVkSWQ9QTA1NDQxOTkyWkI3Wk9aQ0lBM1hZJmVuY3J5cHRlZEFkSWQ9QTA1NTM5OTQ2MTFYWFQ3NDc2TVYmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl)
- 1.3 inch oled display, 128x64 with SH1106-controller using I2C [amazon.com](https://www.amazon.com/HiLetgo-Serial-SSH1106-Display-Arduino/dp/B01MRR4LVE/ref=sr_1_8?dchild=1&keywords=1.3+inch+oled+SH1106&qid=1633087004&sr=8-8)
- IR Temperature Sensor Module (MLX90614) [amazon.com](https://www.amazon.com/MLX90614ESF-Non-Contact-Infrared-Temperature-Arduino/dp/B07YZVDWWB/ref=sr_1_4?dchild=1&keywords=MLX90614&qid=1633084887&sr=8-4)
- 4 momentary push buttons [amazon.com](https://www.amazon.com/Uxcell-a11111400ux0132-Momentary-Tactile-Button/dp/B0090VQLDK/ref=sr_1_43?dchild=1&keywords=momentary+pcb+button+12x12&qid=1633085737&sr=8-43)


## Case
The case is 3D-printed and screwed together. At the moment there are only source-files 
made with OpenSCAD but the plan is to include STL-files too.
