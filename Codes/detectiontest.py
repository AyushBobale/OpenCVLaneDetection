import cv2
import numpy as np

target_img = cv2.imread('images/target2.png',cv2.IMREAD_UNCHANGED)
object_img = cv2.imread('images/fronteg.jpg',cv2.IMREAD_UNCHANGED)




result = cv2.matchTemplate(target_img, object_img, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

print(result)

object_img_w = object_img.shape[1]
object_img_h = object_img.shape[0]

print(max_loc, max_val)
top_left = max_loc
bottom_right = (top_left[0] + object_img_w, top_left[1] + object_img_h)
def drawBox(target_img, top_left, bottom_right):
    cv2.rectangle(target_img, top_left, bottom_right, 
                    color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)

def resize(result, n):
    target_w = result.shape[1]
    target_h = result.shape[0]
    target_sw = int(target_w * n)
    target_sh = int(target_h * n)
    resized_target = cv2.resize(target_img, (target_sw,target_sh), interpolation=cv2.INTER_AREA)
    return resized_target

#result = resize(target_img, 0.5)

#Today 

threshold = 0.39
locations = np.where(result >= threshold)
locations = list(zip(*locations[::-1]))
print(locations)

#end today

cv2.imshow('Result', target_img)
cv2.waitKey()
cv2.destroyAllWindows()