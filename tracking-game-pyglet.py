import math
import random
import sys
import win32api
from win32api import GetSystemMetrics

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import primitives
import utils


class PrimaryWindow(pyglet.window.Window):

    timeLimitSeconds = 5
    FPS = 60
    smoothConfig = utils.get_smooth_config()
    scoreHistoryFile = 'score_history.txt'

    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    trackAreaWidthPixels = 100
    targetRadiusPixels = 20
    targetVelocityX = 2
    targetColor = (0, 128/255, 255/255, 1)
    targetVirtualPositionX = trackAreaWidthPixels/2
    targetDestinationPositionX = 0
    targetDestinationMinimumDistance = 10

    cursorRadiusPixels = 5
    cursorColor = (255/255, 0, 0, 1)

    hitCount = 0
    totalFrames = 0

    mousePressed = False
    paused = True
    firstFrameRendered = False

    def __init__(self):
        super(PrimaryWindow, self).__init__(config=self.smoothConfig, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
        self.set_caption('Tracking Game')
        self.set_size(self.screenWidth, self.screenHeight)
        self.set_mouse_visible(False)
        win32api.SetCursorPos((int(self.screenWidth / 2), int(self.screenHeight / 2)))

        self.target = primitives.Circle(self.screenWidth / 2, self.screenHeight / 2, width=self.targetRadiusPixels * 2, color=self.targetColor)
        self.cursor = primitives.Circle(self.screenWidth/2, self.screenHeight/2, width=self.cursorRadiusPixels*2, color=self.cursorColor)

        self.accuracyLabel = pyglet.text.Label(font_name='Times New Roman',
                                               font_size=36,
                                               x=self.screenWidth/2, y=self.screenHeight/2 - 100,
                                               anchor_x='center', anchor_y='center')


        pyglet.clock.schedule_interval(self.update, 1.0/self.FPS)
        pyglet.app.run()



    def on_draw(self):
        self.clear()
        self.target.render()
        self.cursor.render()
        self.accuracyLabel.draw()

    def on_mouse_motion(self, x, y, dx, dy):

        # Don't capture mouse motion data until after the first frame has been rendered to ignore the mouse position
        # change when the cursor is moved to the middle of the screen.
        if self.firstFrameRendered:
            self.target.x -= dx
            self.target.y -= dy

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.target.x -= dx
        self.target.y -= dy

    def on_mouse_press(self, x, y, button, modifiers):

        if button == mouse.LEFT:
            self.mousePressed = True

        if button == mouse.RIGHT:
            self.paused = not self.paused
            self.accuracyLabel.text = ''

    def on_mouse_release(self, x, y, button, modifiers):

        if button == mouse.LEFT:
            self.mousePressed = False

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            sys.exit(0)


    def update(self, dt):

        # Set the flag indicating that the first frame has been rendered.
        if not self.firstFrameRendered:
            self.firstFrameRendered = True


        # Do nothing if the game is paused.
        if self.paused:
            return


        # Change the target's direction if it reached its destination.
        if self.targetVelocityX > 0 and self.targetVirtualPositionX > self.targetDestinationPositionX:
            self.targetVelocityX *= -1
            self.targetDestinationPositionX = random.random()*(self.targetVirtualPositionX - self.targetDestinationMinimumDistance)

        elif self.targetVelocityX < 0 and self.targetVirtualPositionX < self.targetDestinationPositionX:
            self.targetVelocityX *= -1
            self.targetDestinationPositionX = (self.trackAreaWidthPixels - self.targetVirtualPositionX - self.targetDestinationMinimumDistance)*random.random() + self.targetVirtualPositionX + self.targetDestinationMinimumDistance


        # Move the target.
        self.target.x += self.targetVelocityX
        self.targetVirtualPositionX += self.targetVelocityX

        # Check to see if the target was hit this frame.
        if self.mousePressed and math.sqrt(pow(self.target.x - self.cursor.x, 2) + pow(self.target.y - self.cursor.y, 2)) < self.targetRadiusPixels:
            self.hitCount += 1
        
        self.totalFrames += 1


        # End the game once the time limit is reached.
        if self.totalFrames / self.FPS > self.timeLimitSeconds:
            self.paused = True
            accuracyStr = str(round(self.hitCount/self.totalFrames*100, 2))
            self.accuracyLabel.text = accuracyStr
            utils.write_line(self.scoreHistoryFile, accuracyStr)

            self.hitCount = 0
            self.totalFrames = 0





if __name__ == '__main__':
    PrimaryWindow()
