import os
import cv2
import win32api
from .recognizer import extractSockArea
from .db import isNameExist, insert_info
from tkinter import *

# Function to alert dialog
def showDialog(img):
	root=Tk()
	labelBox=Label(root,text="Please insert name.", height=1, width=20)
	labelBox.pack(padx=5,pady=5)
	textBox=Text(root, height=1, width=20)
	textBox.pack(padx=10,pady=10)
	buttonCommit=Button(root, height=1, width=10, text="save", 
						command=lambda: save_by_name(img, root, textBox))
	buttonCommit.pack(pady=5)
	mainloop()

# Function to save new sock model by name
def save_by_name(img, root, inputbox):
	filename=inputbox.get("1.0","end-1c")
	if filename:
		ret = isNameExist(filename)
		print (ret)
		if not isNameExist(filename):
			# img = extractSockArea(img)
			sift = cv2.xfeatures2d.SIFT_create()
			kp, des = sift.detectAndCompute(img,None)
			insert_info(filename, des)
			root.destroy()
			win32api.MessageBox(0, "Save Success.","Notice")
		else:
			win32api.MessageBox(0, "Filename already exist.\nPlease select other name.","Caution")
	else:
		win32api.MessageBox(0, "Please insert name.","Caution")
