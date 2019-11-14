import cv2
import numpy as np
from matplotlib import pyplot as plt

BLUR = 21
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 250
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
MASK_COLOR = (0.0,0.0,1.0) # In BGR format
MARGIN = 10 # Margin of extract sock 

def extractSockArea(img):
    frame = img
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    # Edge detection 
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)
   
   # Find contours in edges, sort by area 
    contour_info = []
    _, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
   
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    # Create empty mask, draw filled polygon on it corresponding to largest contour 
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    # Smooth mask, then blur it
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    # Blend masked img into MASK_COLOR background 
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = img.astype('float32') / 255.0                 #  for easy blending

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    edged = cv2.Canny(masked, 10, 250)
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    idx, xmin, xmax, ymin, ymax = 0, 0, 0, 0, 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w>50 and h>50:
            if idx == 0:
                xmin, ymin = x, y
            if xmin > x:
                xmin = x
            if ymin > y:
                ymin = y
            if xmax < x+w:
                xmax = x+w
            if ymax < y+h:
                ymax = y+h
            idx += 1

    img = frame[ymin-MARGIN:ymax+MARGIN, xmin-MARGIN:xmax+MARGIN]
    return img