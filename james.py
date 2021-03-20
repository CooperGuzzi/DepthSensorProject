from turtleAPI import robot
import cv2
import rospy
import matplotlib as plt
import numpy as np
import math


def getDepthImg(r):
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
	return temp

def getMask(light, dark, img):
	hsv_test = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    	mask = cv2.inRange(hsv_test, light, dark)
	cv2.imwrite('mask.jpg',mask)	

	return mask	

def findCoM(light, dark, img):

    mask = getMask(light, dark, img)

    array = np.zeros(len(mask[0]))
    num = 0

    for col in range(len(mask[0])):
        for row in range(len(mask)):
            array[col] += mask[row,col]
            num += mask[row,col]

    sum = 0
    i = 0
    for x in array:
        sum += x*i
        i +=1


    if (num!=0):
        x = sum/num

    if not (math.isnan(x)):
        for row in range(len(mask)):
            mask[row,int(x)] = 0

    print(x)

    cv2.imwrite("mask.jpg", mask)

    return x

def getBalloonDepth(light, dark, r):

	depthImg = getDepthImg(r)
	mask = getMask(light, dark, r.getImage())

	print("depth: " + str(len(depthImg)) + "x" + str(len(depthImg[0]))) 	
	print("mask: " + str(len(mask)) + "x" + str(len(mask[0]))) 
	
	balloonDepth = cv2.bitwise_and(depthImg, depthImg, mask = mask)
	cv2.imwrite('bDepth.jpg',balloonDepth)

	return balloonDepth	
	

color = raw_input("Color? ")

if color == 'green':
    light = (40,15,20)
    dark = (80,255,235)

if color == 'purple':
    light = (140,15,20)
    dark = (165,255,235)

if color == 'red':
    light = (0,20,50)
    dark = (8,255,235)

if color == 'yellow':
    light = (25,15,20)
    dark = (40,255,235)

if color == 'blue':
    light = (100,15,20)
    dark = (130,255,235)


r = robot()

img = getBalloonDepth(light, dark, r)
print(img[200,0][0]*10.0/255.0)


