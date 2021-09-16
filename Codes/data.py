class MyData:
    def __init__(self):
        self.fps = 'N/A'
        self.inlane = False
        self.surety = False
        self.slopes = []
        self.fitexits = False
        
    def setFps(self, fps):
        self.fps = fps
    
    def setSurety(self, surety):
        self.surety = surety
    
    def inLane(self, inlane):
        self.inlane = inlane
        
    def setSlopes(self, slopes):
        self.slopes = slopes

    def setFitexists(self, fitexists):
        self.fitexits = fitexists