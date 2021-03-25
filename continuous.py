from turtleAPI import robot
import cv2
import rospy
import matplotlib as plt
import numpy as np
import math
	
def withinDist(minDist, target):
        if minDist > target:
                return False
        else:
                return True
        
def getMinDist(depth):
	row = 0
        minDist = depth[0,0]
        if math.isnan(minDist):
                minDist = 10
        for x in depth:
                for y in x:
			if row > 300:
				break
                        if minDist > y:
                                if math.isnan(y):
                                        y = 10
                                minDist = y
		row += 1
        return minDist

try:
        
        r = robot()
	r.stop()
        depth = r.getDepth()
        r.drive(angSpeed=0, linSpeed=.25)
        ros = rospy.Rate(10)
        while not rospy.is_shutdown():
                ros.sleep()
                depth = r.getDepth()
                minDist = getMinDist(depth)
		print(minDist)
		r.drive(angSpeed=0, linSpeed=.25)
		if withinDist(minDist, 1.5) and not withinDist(minDist, .5):
			r.drive(angSpeed=.5, linSpeed=.1)
                if withinDist(minDist, .5):
                        #r.stop()
			r.drive(angSpeed=-2, linSpeed=-.1)
        
except Exception as e:
        print(e)
        #rospy.loginto("node now terminated")
