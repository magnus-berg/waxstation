from machine import I2C
from displaydriver import DisplayDriver
from imagebuffer import ImageBuffer
from time import sleep_ms as sleep
import sfb_14
import usys

class Display:
    def __init__(self, i2c):
        #try:
        #i2c = I2C(1, sda=sda, scl=scl, freq=400000)
        
        self.display = DisplayDriver(128, 64, i2c, None, 0x3c)
        self.display.rotate(0x01)
        self.display.sleep(False)
        self.display.invert(0x00)
        self.flashScreen()
        #except:
#            print("Failed to init display")
    def flashScreen(self):
        self.display.setFont(sfb_14)
        #self.display.blit(ImageBuffer().getLogo(), 0, 10)
        self.display.blit(ImageBuffer().getImage('logo'), 0, 0)
        self.display.show()
        sleep(300)
        #self.display.text("WAXstation", 23, 40)
        self.display.text("WAXstation 1000", 1, 40)
        self.display.text("v1.0", 44, 92)
        self.display.show()
        sleep(1500)
        
        self.display.clear()
        #self.display.invert(0x00)
        self.display.show()

    def poweroff(self):
        try:
            self.display.poweroff()
        except:
            print("Failed to power off display")
            usys.exit()
    def poweron(self):
        try:
            self.display.poweron()
        except:
            print("Failed to power on display")
            usys.exit()
            
    def show(self):
        try:
            self.display.show()
        except:
            print("Display error (show)")
            usys.exit()
            
    def setFont(self, font):
        self.display.setFont(font)
            
    def clear(self):
        try:
            self.display.clear()
        except:
            print("Display error (clear)")
            usys.exit()
    def size(self, text):
        return self.display.writer.stringlen(text)
    
    def text(self, text, x, y):
        self.display.text(text, x, y)

    def image(self, name, x, y):
        img = ImageBuffer().getImage(name)
        self.display.blit(img, x, y)