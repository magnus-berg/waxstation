# DisplayDriver for SH1106 using i2c

from micropython import const
import utime as time
import framebuf
from writer import Writer
import sf_14

# a few register definitions
_SET_CONTRAST        = const(0x81)
_SET_NORM_INV        = const(0xa6)
_SET_DISP            = const(0xae)
_SET_SCAN_DIR        = const(0xc0)
_SET_SEG_REMAP       = const(0xa0)
_LOW_COLUMN_ADDRESS  = const(0x00)
_HIGH_COLUMN_ADDRESS = const(0x10)
_SET_PAGE_ADDRESS    = const(0xB0)





class DisplayDriver(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, res=None, addr=0x3c):
        super
        self.width = width
        self.height = height
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        
        self.i2c = i2c
        self.addr = addr
        self.res = res
        self.temp = bytearray(2)
        if res is not None:
            res.init(res.OUT, value=1)

        
        super().__init__(self.buffer, self.width, self.height, framebuf.MVLSB)
        self.writer = Writer(self, sf_14)
        self.init_display()

    def init_display(self):
        self.reset()
        self.fill(0)
        self.poweron()
        self.show()

    def poweroff(self):
        self.write_cmd(_SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(_SET_DISP | 0x01)

    def rotate(self, flag, update=True):
        if flag:
            self.write_cmd(_SET_SEG_REMAP | 0x01)  # mirror display vertically
            self.write_cmd(_SET_SCAN_DIR | 0x08)  # mirror display hor.
        else:
            self.write_cmd(_SET_SEG_REMAP | 0x00)
            self.write_cmd(_SET_SCAN_DIR | 0x00)
        if update:
            self.show()
            
    def clear(self):
        self.fill(0x00)

    def sleep(self, value):
        self.write_cmd(_SET_DISP | (not value))

    def contrast(self, contrast):
        self.write_cmd(_SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(_SET_NORM_INV | (invert & 1))

    def show(self):
        for page in range(self.height // 8):
            self.write_cmd(_SET_PAGE_ADDRESS | page)
            self.write_cmd(_LOW_COLUMN_ADDRESS | 2)
            self.write_cmd(_HIGH_COLUMN_ADDRESS | 0)
            self.write_data(self.buffer[
                self.width * page:self.width * page + self.width
            ])

    def reset(self):
        if self.res is not None:
            self.res(1)
            time.sleep_ms(1)
            self.res(0)
            time.sleep_ms(20)
            self.res(1)
            time.sleep_ms(20)
            
    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40'+buf)
        
    def setFont(self, font):
        self.writer = Writer(self, font, False)
        
    def text(self, string, x, y):
        Writer.set_textpos(self, y, x)
        self.writer.printstring(string)


class DBuffer(framebuf.FrameBuffer):
    def __init__(self, width=128, height=128):
        super
        self.width = width
        self.height = height
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        
        self.temp = bytearray(2)
 
        super().__init__(self.buffer, self.width, self.height, framebuf.MVLSB)


    def setFont(self, font):
        self.writer = Writer(self, font, False)

    def text(self, string, x, y):
        Writer.set_textpos(self, y, x)
        self.writer.printstring(string)

    def centeredText(self, string, y):
        size = self.writer.stringlen(string)
        x = int((self.width-size)/2)
        self.text(string, x, y)