import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import time
import my_utils

def grab_screen(region = None, name = None):

    #hwin = win32gui.GetDesktopWindow()

    #Test Block -------
    
	
    hwin  = win32gui.FindWindow(None, name)
    if not hwin:
        print("Window not found")
        return
    
    if name is None:
        hwin = win32gui.GetDesktopWindow()
	
    if region:
        left,top,x2,y2 = region
        border_pixels = 8
        titlebar_pixels = 30
        top = top + titlebar_pixels + border_pixels
        left = left + border_pixels
        width = x2 - left + 1 
        height = y2 - top + 1  + titlebar_pixels
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    
    

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)



def show_grab():

    winname = 'Grand Theft Auto V'
    height = 790
    width = 590
    while True:
        start = time.time()
        screen = grab_screen(region=(0, 0, height, width), name= winname)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        cv2.imshow(" - Clone", screen)
        #print("FPS : ", 1000/(time.time() - start + 0.00001))
        if cv2.waitKey(1) == ord('q'):
            break
        
    cv2.destroyAllWindows()

#show_grab()



