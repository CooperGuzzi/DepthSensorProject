from turtleAPI import robot
import cv2
import rospy
import matplotlib as plt
import numpy as np
import math

def get_ang_err(com, P=.5):
    return P*(320-com)

def get_dist_err(dens,P=.5):
    return P*(921600-dens)

def augmentedImg(image, mask, color):
    if color == 'blue' or color == 'pink':
        # apply blue filter
        image[:,:,0] = np.bitwise_or(image[:,:,0], mask)
    if color == 'yellow' or color == 'green':
        # apply green filter
        image[:,:,1] = np.bitwise_or(image[:,:,1], mask)
    if color == 'pink' or color == 'red' or color == 'yellow':
        # apply red filter
        image[:,:,2] = np.bitwise_or(image[:,:,2], mask)

    return image

def getMask(light, dark, img):
	hsv_test = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    	mask = cv2.inRange(hsv_test, light, dark)
        mask = cv2.fastNlMeansDenoising(mask, mask, 100, 7, 21)
        ret, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
	cv2.imshow('mask.jpg',mask)
        cv2.waitKey(1)
	return mask

def findCoM(light, dark, img, mask):

    #mask = getMask(light, dark, img)

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

    #print(x)

    #cv2.imwrite("mask.jpg", mask)

    return x

def getBalloonDist(mask, depth):
       	totDist = 0
        numPixels = 0
        xx = 0
        yy = 0
        for x in mask:
                for y in x:
                        if y[0] == 255:
                                totDist += depth[xx, yy]
                                numPixels += 1
                        yy += 1
                        
                yy = 0
                xx += 1
        return totDist/numPixels
        

######################

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
    light = (105,0,0)
    dark = (115,255,255)

r = robot()


#img_rgb = r.getImage()
#cv2.imwrite('test.jpg',img_rgb)
#img_hsv = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2HSV)
#cv2.imwrite('before.jpg',img_hsv)
#outhsv = cv2.inRange(img_hsv,light,dark)
#cv2.imwrite('after.jpg',outhsv)



ros = rospy.Rate(10)

while not rospy.is_shutdown():
    img = r.getImage()
    dpth = r.getDepth()
    mask = getMask(light, dark, img)
    augmented = augmentedImg(img, mask, color)
    cv2.imshow('augmented', augmented)
    cv2.waitKey(1)
    bDist = getBalloonDist(mask, dpth)
    print("distance: " + str(bDist))
    #err = 320-findCoM(light,dark,img)
    #if err > .2:
        #err = .2
    #if err < -.2:
        #err = -.2
    #if err==0:
        #r.drive(angSpeed=3,linSpeed=0)
    #else:
        #r.drive(angSpeed=err*(bDist/10),linSpeed=.1)
	#if bDist < .8:
		#break    
    ros.sleep()

r.stop()
