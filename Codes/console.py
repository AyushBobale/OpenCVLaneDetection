import cv2
import numpy as np
import time
from numba import jit

class ConsoleData:
    def __init__(self, name):
        self.console = np.zeros([300,650,1],dtype=np.uint8)
        self.name = name 
        self.fontsize = 0.8
        self.fontthickness = 0
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontcolor = (125,10,255)
        self.accuraccy = 'N/A'
        self.diff = 0
    
    def show(self):
        cv2.imshow(self.name, self.console)
        
    def setFPS(self, fps):
        self.fps = fps
        cv2.putText(self.console, "FPS : " + str(self.fps), (0,20),
                    self.font,
                    self.fontsize,
                    self.fontcolor,
                    self.fontthickness,
                    cv2.LINE_AA)
    
    def setSurety(self, surety):
        self.surety = surety
        cv2.putText(self.console, "No fit : " + str(not self.surety), (0,70),
                    self.font,
                    self.fontsize,
                    self.fontcolor,
                    self.fontthickness,
                    cv2.LINE_AA)
    
    def inLane(self, inlane):
        self.inlane = inlane
        cv2.putText(self.console, "If in Lane : " + str(self.inlane), (255,20),
                    self.font,
                    self.fontsize,
                    self.fontcolor,
                    self.fontthickness,
                    cv2.LINE_AA)
    
    def setSlopes(self, slopes):
        self.slopes = slopes
        #self.accuraccy = 'TO BE DONE'
        cv2.putText(self.console, "Slopes : " + str(self.slopes), (0,120),
                    self.font,
                    self.fontsize,
                    self.fontcolor,
                    self.fontthickness,
                    cv2.LINE_AA)
    
    def calcAccuraccy(self):
        self.diff = abs(self.slopes[0]) + abs(self.slopes[1])
        self.accuraccy = ((19 - abs(self.diff) + 0.000001)/19) * 100
        cv2.putText(self.console, "Accuraccy : " + str(round(self.accuraccy, 5)) + "%", (255,70),
                    self.font,
                    self.fontsize,
                    self.fontcolor,
                    self.fontthickness,
                    cv2.LINE_AA)
    
    def ifFitDoesNotExists(self):
        self.console.fill(0)
        cv2.putText(self.console, "Could not detect lanes !!!" , (0,120),
                    self.font,
                    self.fontsize,
                    self.fontcolor,
                    self.fontthickness,
                    cv2.LINE_AA)

    def ifFitDoesExists(self):
        self.console.fill(0)



def run():
    newConsole = ConsoleData("Console")
    latency = 0
    while True:
        start_time = time.time()
        if cv2.waitKey(1) == ord('c'):
            break
        newConsole.setFPS(latency)
        newConsole.setSurety(True)
        #newConsole.ifFitDoesNotExists()
        newConsole.inLane(True)
        newConsole.setSlopes([-0.5, 1])
        newConsole.calcAccuraccy()
        
        #print(newConsole.accuraccy, "\n", newConsole.diff, "\r")
        newConsole.show()
        newConsole.ifFitDoesExists()
        latency = time.time() - start_time
#---------------------------------------------------Debug not active
#run()