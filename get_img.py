from turtleAPI import robot
import cv2
import rospy
import matplotlib as plt
import numpy as np
import math

r = robot()

depth_img = r.getDepth()
temp = r.getImage()

print(depth_img[0,0])

row = 0
col = 0
for x in depth_img:
	for y in x:
		if math.isnan(y):
			y = 0
		temp[row,col] = (y/10)*255
		col += 1	
	row += 1
	col = 0

cv2.imwrite('depth.jpg',temp)
