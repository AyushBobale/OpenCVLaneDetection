from fpdf import FPDF
import os

def calcFrame(lst):
    return len(lst) / (sum(lst) + 0.0001)

class Benchmark:
    def __init__(self):
        self.framecount = 1
        self.totLatency = 1
        self.notInLane = 0
        self.inLane = 0
        self.totAcccuracy = 0
        self.latencyList = []
        self.noFit = 0
        self.fit = 0

    def updateVals(self, latency, inlane, fit, slopes):
        self.totLatency +=  latency
        self.latencyList.append(latency)
        self.framecount += 1
        
        if inlane:
            self.inLane += 1
        else :
            self.notInLane += 1
        
        if fit:
            diff = abs(slopes[0]) + abs(slopes[1])
            accuracy = ((19 - abs(diff) + 0.000001)/19) * 100
            self.totAcccuracy += accuracy
            self.fit += 1
        else:
            self.noFit += 1
    
    def givenData(self, win_name, resox, resoy, scale_factor, min_neighbour, peds, cars):
        self.win_name = win_name
        self.resox = resox
        self.resoy = resoy
        self.scale_factor = scale_factor
        self.min_neighbour = min_neighbour
        if peds : 
            self.peds = 'Enabled'
        else:
            self.peds = 'Disabled'
        if cars : 
            self.cars = 'Enabled'
        else:
            self.cars = 'Disabled'
        if self.win_name is None:
            self.win_name = 'Desktop'

    def printBench(self):
        self.latencyList.sort()
        self.latencyList.reverse()
        self.percentile10 = calcFrame(self.latencyList[ 0 : int(len(self.latencyList) * 0.1 ) : 1])
        self.percentile1  = calcFrame(self.latencyList[ 0 : int(len(self.latencyList) * 0.01 ) : 1])
        self.percentile01 = calcFrame(self.latencyList[ 0 : int(len(self.latencyList) * 0.001 ) : 1])
        print('10th percentile : ', self.percentile10)
        print('1st percentile : ', self.percentile1)
        print('0.1 percentile : ', self.percentile01)
        print('Frame : ', self.framecount, ' Avg FPS : ', (self.framecount/ self.totLatency), ' In lane : ', self.inLane, ' Not in Lane :', self.notInLane, 
                ' AVG Accuracy : ', (self.totAcccuracy / (self.fit + 1)), ' Fit : ', self.fit, ' No fit : ', self.noFit)

    def reportGen(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", 'B' ,size = 15)
        pdf.cell(200, 10, txt = "Usage Statistics Report", ln = 1, align = 'L')
        pdf.set_font("Times", size = 10)
        pdf.cell(200, 10, txt = "The following are some usage parameters of the last run.",ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "",ln = 1, align = 'L')

        pdf.set_font("Times", size = 9)
        pdf.cell(95, 7, txt = "Window Name :- " + str(self.win_name) ,ln = 1, align = 'L', border = 0)
        pdf.cell(95, 7, txt = "Resolution  :- " + str(self.resox) + ', ' + str(self.resoy) ,ln = 1, align = 'L', border = 0)
        pdf.cell(95, 7, txt = "Scale Factor :- " + str(self.scale_factor)  ,ln = 1, align = 'L', border = 0)
        pdf.cell(95, 7, txt = "Minimum Neighbour :- " + str(self.min_neighbour)  ,ln = 1, align = 'L', border = 0)
        pdf.cell(95, 7, txt = "Cars :- " + str(self.cars)  ,ln = 1, align = 'L', border = 0)
        pdf.cell(95, 7, txt = "Pedestrians  :- " + str(self.peds)  ,ln = 1, align = 'L', border = 0)
        pdf.cell(95, 7, txt = "Total time test ran :- " + str(self.totLatency) + 'ms' ,ln = 1, align = 'L', border = 0)
        pdf.cell(200, 5, txt = "",ln = 1, align = 'L')
        pdf.cell(200, 5, txt = "",ln = 1, align = 'L')

        pdf.set_font("Times", size = 8)

        

        pdf.cell(200, 5, txt = "",ln = 1, align = 'L')

        pdf.cell(95, 6, txt = "Total Frame count  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.framecount) ,ln = 1, align = 'L', border = 1)

        pdf.cell(95, 6, txt = "Average Frames / Second  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.framecount / self.totLatency) ,ln = 1, align = 'L', border = 1)

        pdf.cell(95, 6, txt = "No of Frames in Lane  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.inLane) ,ln = 1, align = 'L', border = 1)

        pdf.cell(95, 6, txt = "No of Frames not in lane  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.notInLane) ,ln = 1, align = 'L', border = 1)

        pdf.cell(95, 6, txt = "Average Accuracy  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.totAcccuracy / (self.fit + 1)) + '%' ,ln = 1, align = 'L', border = 1)

        pdf.cell(95, 6, txt = "No of Frames Fit existed  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.fit) ,ln = 1, align = 'L', border = 1)
        
        pdf.cell(95, 6, txt = "No of Frames Fit did notexisted  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.noFit) ,ln = 1, align = 'L', border = 1)

        pdf.cell(95, 6, txt = "10th Percentile FPS  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.percentile10) ,ln = 1, align = 'L', border = 1)

        pdf.cell(95, 6, txt = "1st Percentile FPS  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.percentile1) ,ln = 1, align = 'L', border = 1)

        pdf.cell(95, 6, txt = "0.1th Percentile FPS  "  ,ln = 0, align = 'L', border = 1)
        pdf.cell(95, 6, txt =  str(self.percentile01) ,ln = 1, align = 'L', border = 1)

        pdf.output("Report.pdf")
        os.startfile("Report.pdf")


#========================================
#Do some optimizations with canny params for threshold
#Watch  the video in the playlist report gren funtionality is to be added and making exe file
#=========================================