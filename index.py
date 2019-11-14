import os
import cv2
import win32api
import numpy as np

from source.dialog import showDialog
from source.detecter import scanSock
from source.recognizer import extractSockArea


# keycode
KeyEsc = 27     # ESC 
KeyEnter = 13   # Enter 
KeySpace = 32   # Space 

# Function to open camera if device is connected
def openCamera():
    cam = cv2.VideoCapture(cv2.CAP_DSHOW)

    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False
        win32api.MessageBox(0,"Please connect camera.","Notice")

    while rval:
        cv2.imshow("Sock Analaysis System", frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)

        if key == KeySpace:
            data = scanSock(frame)
            if data['isSame']:
                win32api.MessageBox(0,"Sock Name : %s"%data['sockName'],"Notice")
            else:
                result = win32api.MessageBox(0,"No exist in sock list. \nDo you want add this sock to list?","Notice", 1)
                if result == 1:
                    showDialog(frame)

        if key == KeyEsc:  
            rval = False
        # if key == KeyEnter:
        #     img = cv2.imread(os.path.join(ModelPath, '1.jpeg'))
        #     img = extractSockArea(img) 
        #     cv2.imwrite(os.path.join(ModelPath, 'test.jpeg'), img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    openCamera()