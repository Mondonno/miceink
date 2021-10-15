from misc.utils import *
from misc.constants import *
from misc.tags import EventTagger

from datetime import datetime
 
class MiceInkEvents():
    # defining the tagger that will tag all event functions
    eventTag = EventTagger()

    def __init__(self, parent):
        self.data = parent.data # THIS SHOULD BE REFERENCE
        self.mainParent = parent.parent # THIS SHOULD BE REFERENCE

    def getEvents(self):
        return self.eventTag.registredEvents;

    @eventTag("MouseMotion")
    def MouseMotion(self, screen, event):
        pgGUI = self.mainParent.getPygame()
        (mX, mY) = pgGUI.mouse.get_pos()

        if self.data.currentX == None or self.data.currentY == None:
            self.data.currentX = mX
            self.data.currentY = mY
                
        speed = getSpeedOfPoints(self.data.currentX,
            self.data.currentY,
            mX, mY,
            self.data.lastTime)

        if self.data.lastSpeed != None:
            consistency = abs(self.data.lastSpeed - speed)

        if (self.data.lastSpeed != None
            and consistency <= TOUCH_PAD_MACOS_CONSISTENCY
            and self.data.mouseStatus == False):
            self.data.penOn = True
        elif self.data.penOn == True:
            self.data.penOn = False

        if self.data.penOn == True:
            if BRUSH_TYPE == 0:
                pygame.draw.circle(screen,
                    BRUSH_COLOR,
                    (mX, mY),
                    self.data.brushSize)
            else:
                pygame.draw.line(screen, BRUSH_COLOR, 
                    (self.data.currentX, self.data.currentY),
                    (mX, mY),
                    width=self.data.brushSize)

        self.data.lastTime = datetime.now()
        self.data.lastSpeed = speed

        self.data.currentX = mX
        self.data.currentY = mY

    @eventTag("MouseButtonDown")
    def MouseButtonDown(self, screen, event):
        if self.data.mouseStatus:
            self.data.mouseStatus = False
        else:
            self.data.mouseStatus = True

    @eventTag("KeyDown")
    def KeyDown(self, screen, event):
        pyGUI = self.mainParent.getPygame()

        if event.key == pyGUI.K_s:
            saveToPath = createOutputFilePath(SAVE_FILE_PATH, SAVE_FILE_NAME, SAVE_FILE_EXT)
            pyGUI.image.save(screen, saveToPath)

        if event.key == pyGUI.K_c:
            self.mainParent.fillDisplay()

    @eventTag("Quit")
    def AppQuit(self, screen, event):
        self.mainParent.running = False