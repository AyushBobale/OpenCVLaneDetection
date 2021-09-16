import  cv2 
import numpy as np
import screengrab
import time
from _collections_abc import Iterable
from multiprocessing import *
from console import ConsoleData
from data import *
from benchmark import Benchmark
#from gui import Attributes


#---------------------Global Vars
IN_LANE = False
NOT_SURE = True
SLOPES = [-0.5, 0.5]
#---------------------Functions

def make_coordinates(image, line_parameters):
    try : 
        slope, intercept = line_parameters
        y1 = image.shape[0]
        y2 = int(y1 *(3/5))
        x1 = int((y1 - intercept)/(slope + 0.000001))
        x2 = int((y2 - intercept)/(slope + 0.000001))
    except TypeError:
        return None
    return np.array([x1, y1, x2, y2])
	

def if_in_lane(left_slope, right_slope):
    global NOT_SURE, IN_LANE, SLOPES
    if len(left_slope) == 1 and len(right_slope) == 1:#      if a fit exists
        NOT_SURE = False
        SLOPES = [round(left_slope[0][0], 2), round(right_slope[0][0], 2)] #------------------------------------Debug
        if left_slope[0][0] < -0.3 or right_slope[0][0] > 0.3: # the value 0.5 is used to set slope limits
            print("Slopes : ", left_slope[0][0], right_slope[0][0])
            IN_LANE = True
        else:
            IN_LANE = False
    else:
        NOT_SURE = True
        
def average_slope_intercept(image, lines):
    global IN_LANE	

    left_fit = []
    right_fit = []

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parmerters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parmerters[0]
        intercept = parmerters[1]
        if slope < 0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    if_in_lane(left_fit,right_fit)
    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 200) # def 50,150
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for  line in lines:
            if line is None:
                continue
            x1, y1, x2, y2  = line.reshape(4)
            try :
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            except OverflowError:
                continue
    return line_image

def region_of_intrest(image):
    height = image.shape[0]
    width = image.shape[1]
    polygons = np.array([
        [(int(width * 0.1), int(height * 0.85)), 
        (int(width * 0.9) , int(height * 0.85)), 
        (int(width * 0.5), int(height * 0.2))]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image
	
def harcascade(frame, cascade, reduction_factor = 1.05, nearest_neighbour=3):
    return cascade.detectMultiScale(frame, reduction_factor, nearest_neighbour)

def draw_rect(rect_list, frame, name='default'):
    for(x, y, w, h) in rect_list:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
        cv2.putText(frame, 
                    name,
                    (x - 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (150,255,20),
                    1,
                    cv2.LINE_AA)

	
#Cascades
car_cascade_src = "Cascades\\Cars\\cars.xml"
car_cascade = cv2.CascadeClassifier(car_cascade_src)
peds_cascade_src = "Cascades\\Peds\\peds.xml"
peds_cascade = cv2.CascadeClassifier(peds_cascade_src)

#Vars -------------------------------------------
X1 = 0
Y1 = 0
X2 = 990 #750#580
Y2 = 480 #400#280
scale_factor = 1.05
min_neighbours = 6
Window_name= None
newConsole = ConsoleData("Debug Console")
myBench = Benchmark()
peds = False
cars = False
myBench.givenData(Window_name, X2, Y2, scale_factor, min_neighbours, peds, cars)

def setValues(params):
    global Window_name, X2, Y2, scale_factor, min_neighbours, cars, peds, myBench
    Window_name = params.win_name
    X2 = int(params.resoX)
    Y2 = int(params.resoY)
    scale_factor = float(params.scale_factor)
    min_neighbours = int(params.min_neighbour)
    peds = params.peds
    cars = params.cars
    #print('In set values ')
    myBench.givenData(params.win_name, params.resoX, params.resoY, params.scale_factor, params.min_neighbour, params.peds, params.cars)
    run()
    print('In set values after run')
    myBench.printBench()
    myBench.reportGen()

#loop
def run():
    while True:
        start_time = time.time()
        if cv2.waitKey(1) == ord('q'):
            break
        frame = screengrab.grab_screen(region=(X1, Y1, X2, Y2), name = Window_name)
        canny_image = canny(frame)
        cropped_image = region_of_intrest(canny_image)
        lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 100, maxLineGap = 5)
        
        if lines is None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            if peds:
                ped_rect_list = harcascade(frame, peds_cascade, scale_factor, min_neighbours)
                draw_rect(ped_rect_list, frame, "PED")
            if cars:
                car_rect_list = harcascade(frame, car_cascade, scale_factor, min_neighbours)
                draw_rect(car_rect_list, frame, "CAR") 


            newConsole.ifFitDoesNotExists()
            newConsole.setFPS(int((1/(time.time() - start_time + 0.00001))))
            newConsole.show()
            #cv2.imshow("Canny ", cropped_image)
            cv2.imshow("Result ", frame)

            #
            lat = time.time() - start_time
            myBench.updateVals(lat, False, False, [])
            #

            continue

        averaged_lines = average_slope_intercept(frame, lines)
        line_image = display_lines(frame, averaged_lines)
        combined_image = cv2.addWeighted(frame, 1, line_image, 1, 1)
        combined_image = cv2.cvtColor(combined_image, cv2.COLOR_BGRA2RGB)
        
        if peds :
            ped_rect_list = harcascade(frame, peds_cascade, scale_factor, min_neighbours)
            draw_rect(ped_rect_list, combined_image, "PED")
        if cars:
            car_rect_list = harcascade(frame, car_cascade, scale_factor, min_neighbours)
            draw_rect(car_rect_list, combined_image, "CAR")
        

        
        newConsole.ifFitDoesExists()
        newConsole.setFPS(int((1/(time.time() - start_time + 0.00001))))
        newConsole.setSlopes(SLOPES)
        newConsole.setSurety(NOT_SURE)
        newConsole.inLane(IN_LANE)
        newConsole.calcAccuraccy()
        newConsole.show()

        #
        lat = time.time() - start_time
        myBench.updateVals(lat,IN_LANE, NOT_SURE, SLOPES)
        #
        #cv2.imshow("Canny ", cropped_image)
        cv2.imshow("Result ", combined_image)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    run()
    myBench.printBench()
    myBench.reportGen()

#make a cropped image of the original frame and then pass it to Harr cascasde to reduce false positive
#run()
#TO CHANGE THE CANNY VARS FOR OPTIMIZATIONS
#myBench.printBench()
#myBench.reportGen()
#setValues('debug')
#made cython file still no improvements
###
