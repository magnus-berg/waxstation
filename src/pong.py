from machine import Pin, SoftI2C, I2C, PWM
from time import sleep_ms as sleep
import random
import framebuf
import math
from image import Image

class Pong:
    class Range:
        def __init__(self, lower, upper):
            self.lower = lower
            self.upper = upper
            
        def verify(self, n):
            return (n >= self.lower and n <= self.upper)
    
    
    class Pad:
        def __init__(self, pong, x):
            self.range = Pong.Range(5, 58)
            self.x = x
            self.reset()
            self.pong = pong
            self.spread = 0
            self.spreadTable = [-7, -7, -5, -4, -4, -3, -3, -3, -2, -2, -2, -2, -1, -1, -1, -1, -1, 7, 7, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1] # 34 positions

        def move(self, pos):
            if self.range.verify(pos):
                self.pos = int(pos)

        def reset(self):
            self.pos = 31
            
        def getDirection(self, ballYPos, dx):
            diff = int(ballYPos) - self.pos
            
            if diff < -7 or diff > 7:
                self.pong.playFailSound()
                # play miss sound
                print("Ball " + str(int(ballYPos)) + " Pad " + str(self.pos))
                return None
            correction = math.pi/18 * diff  # 10 degrees / diff
            print("dX: " + str(dx))
            self.pong.playsound()
            self.spread = self.spreadTable[random.randrange(0, 34)]

            if dx < 0:
                #print("Left")
                return correction
            else:
                #print("Right")
                return math.pi - correction

        
    class Ball:
        def __init__(self, pong, x, y, direction, speed=2.5):
            self.pong = pong
            self.speed = speed
            self.xRange = Pong.Range(1,126)
            self.yRange = Pong.Range(1,62)
            self.reset(direction)
            
        def setDirection(self, angle):
            self.direction = angle
            #print("Direction: " + str(angle) + " X: " + str(self.x) + " Y: " + str(self.y))
            self.dx = self.speed*math.cos(angle)
            self.dy = self.speed*math.sin(angle)

        def reset(self, direction=0):
            self.x = 62.0
            self.y = 30.0
            self.setDirection(direction)
            self.calculateAndSetNextImpact()
            
        def calculateAndSetNextImpact(self):
            _dx = self.dx
            _dy = self.dy

            _x = self.x
            _y = self.y
            
            while self.xRange.verify(_x + _dx):
                _x += _dx
                if self.yRange.verify(_y + _dy):
                    _y += _dy
                else:
                    _dy = -_dy
            self.nextImpact = int(_y)
            #print("Next Impact: " + str(_y))
            
        def next(self, pad1, pad2):
            #print("By:" + str(self.y) + " p1y: " + str(pad1.pos) + " p2y: " + str(pad2.pos))
            
            _x = self.x + self.dx
            _y = self.y + self.dy
            #print("X: " + str(_x) + " Y: " + str(_y))
            if self.xRange.verify(_x) and self.yRange.verify(_y):
                self.x = _x
                self.y = _y
            else:
                if not self.xRange.verify(_x):
                    newDirection = None

                    if self.dx < 0:
                        newDirection = pad1.getDirection(_y, self.dx)
                        self.x = 1
                    else:
                        newDirection = pad2.getDirection(_y, self.dx)
                        self.x = 126
                    if newDirection != None: # miss
                        self.setDirection(newDirection)
                        self.calculateAndSetNextImpact()
                    else:
                        print("MISS!!! pos: " + str(self.y))
                        if self.dx < 0:
                            return 1
                        else:
                            return 0
                        
                if not self.yRange.verify(_y):
                    self.setDirection(-self.direction)               
            return -1
    

    
    def __init__(self, display, pins, soundPin = None):
        self.width = 128
        self.height = 64
        self.ball = self.Ball(self, 62.0, 30.0, 0)
        self.p1 = self.Pad(self, 0)
        self.p2 = self.Pad(self, 127)
        self.reset()
        self.display = display
        
        self.pins = pins
        if soundPin != None:
            self.speaker = PWM(soundPin)
            
            
        self.soundPin = soundPin
        #self.counter = 0
    def reset(self):
        self.score = [8, 8]
        self.ball.reset()
        self.p2.reset()
        
    def getNumberIcon(self, index):
        buffer = bytearray(5)
        for idx, byte in enumerate(self.numbers[index]):
            buffer[idx] = byte
        return framebuf.FrameBuffer(buffer, 5, 7, framebuf.MVLSB)

    def printScore(self):
        self.display.blit(Image.getSymbol(self.score[0]), 52, 1)
        self.display.blit(Image.getSymbol(10), 61, 1)
        self.display.blit(Image.getSymbol(self.score[1]), 70, 1)
        
    @property
    def running(self):
        return self.score[0] < 10 and self.score[1] < 10

    def showWinner(self):
        index = 0 if self.score[0] == 10 else 1

        self.display.clear()
        self.display.blit(Image.getWinnerImage(index), 0, 13)
        self.display.show()
        
    def step(self):
        # cleanup
        self.display.clear()
        self.printScore()        
        # get new position for the pads and ball
        #self.p1.move(self.ball.y+self.ball.dy - 9 - 4 + random.randrange(0, 18))
        
        #self.p2.move(self.ball.y+self.ball.dy  ) ##- 5 + random.randrange(0, 12)
        if self.ball.dx > 0:
            if (self.ball.nextImpact + self.p2.spread) > self.p2.pos:
                self.p2.move(self.p2.pos+1)
            elif (self.ball.nextImpact + self.p2.spread) < self.p2.pos:
                self.p2.move(self.p2.pos-1)
        else:
        #self.p2.move(self.ball.y+self.ball.dy  ) ##- 5 + random.randrange(0, 12)
            if (self.ball.nextImpact + self.p1.spread) > self.p1.pos:
                self.p1.move(self.p1.pos+1)
            elif (self.ball.nextImpact + self.p1.spread) < self.p1.pos:
                self.p1.move(self.p1.pos-1)
            


        p2move = 0
        if self.pins[1].value() == 0:
            p2move = 1
        elif self.pins[0].value() == 0:
            p2move = -1
        
        #self.p2.move(self.p2.pos + p2move)
 
        winner = self.ball.next(self.p1, self.p2)
        if winner > -1:
            self.score[winner] += 1
            print("Miss..." + str(winner))
            self.ball.reset()
            self.p2.reset()
        
        self.display.fill_rect(0, self.p1.pos-5, 1, 10, 0x01)
        self.display.fill_rect(127, self.p2.pos-5, 1, 10, 0x01)
        self.display.fill_rect(int(self.ball.x-1), int(self.ball.y-1), 2, 2, 0x01)
        self.display.show()
        
    def playsound(self, note=440):
        if self.speaker == None:
            return
        self.speaker.duty_u16(int(65536/2))
        self.speaker.freq(note)
        sleep(10)
        self.speaker.duty_u16(0)

    def playFailSound(self):
        if self.speaker == None:
            return
        self.speaker.duty_u16(int(65536/2))
        for f in range(0, 600, 15):
            self.speaker.freq(880-f)
            sleep(8)
        self.speaker.duty_u16(0)
        
    def run(self):
        self.display.poweron()
        kill = self.pins[3].value() == 0 and self.pins[2].value() == 0 and self.pins[1].value() == 0 and self.pins[0].value() == 0
        while not kill:
            while self.running and not kill:
                self.step()

            self.showWinner()
            restartGame = False
            while not restartGame:
                for p in self.pins:
                    if p.value() == 0:
                        restartGame = True
            self.reset()
            
            