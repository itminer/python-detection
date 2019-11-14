import os
import cv2
import win32api
from tkinter import *
from .dialog import showDialog
from .db import get_all

MIN_MATCH_COUNT = 100 # matched point 

# Function to compare two sock whether is the same or not
def isSameSock(des1, des2):
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks = 50)

	flann = cv2.FlannBasedMatcher(index_params, search_params)
	matches = flann.knnMatch(des1,des2,k=2)

	good = []
	for m,n in matches:
		if m.distance < 0.7*n.distance:
			good.append(m)
	if len(good) > MIN_MATCH_COUNT:
		return True
	else:
		return False
	print ("%d matched between two images." %len(good))

# Function to get all sock model and compare those with image captured from camera
def scanSock(img):
	sockList = []
	data = {"isSame" : False}
	sockList = get_all()
	if not (len(sockList)>0):
		return data
	
	sift = cv2.xfeatures2d.SIFT_create()
	kp1, input_des = sift.detectAndCompute(img,None)
	
	for sockinfo in sockList:
		model_des = sockinfo[2]
		ret = isSameSock(input_des, model_des)
		if ret:
			data = {
				"isSame" : True,
				"sockName" : sockinfo[1] 
			}
			return data
	return data
