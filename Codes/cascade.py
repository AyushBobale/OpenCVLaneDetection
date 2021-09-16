import cv2
import screengrab
import time

car_cascade_src = "Cascades\\Cars\\cars.xml"

car_cascade = cv2.CascadeClassifier(car_cascade_src)

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny_image = cv2.Canny(blur, 50, 150)
    return canny_image

X1 = 0
Y1 = 0
X2 = 745
Y2 = 385
Window_name = "POCO F1"


while True:
    start = time.time()
    if cv2.waitKey(1) == ord('q'):
        break
    frame = screengrab.grab_screen(region=(X1, Y1, X2, Y2), name = Window_name)
    #canny_image = canny(frame)
    cars = car_cascade.detectMultiScale(frame, 1.5, 5)
    for(x, y, w, h) in cars:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("Cascade", frame)
    print("Frame time : " + str(1/ (time.time() - start + 0.000001)))
    
cv2.destroyAllWindows()	