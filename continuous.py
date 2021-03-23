from turtleAPI import robot
import cv2
import rospy
import matplotlib as plt
import numpy as np
import math
	
def withinDist(depth):
        minDist = depth[0,0]
        if math.isnan(minDist):
                minDist = 10
        for x in depth:
                for y in x:
                        if minDist > y:
                                if mat.isnan(y):
                                        y = 10
                                minDist = y
        if minDist > 0.5:
                return False
        else:
                return True

try:
        
        r = robot()
        depth = r.getDepth()
        r.drive(angSpeed=0, linSpeed=.25)
        ros = rospy.Rate(10)
        while not rospy.is_shutdown():
                ros.sleep()
                depth = r.getDepth()
                if withinDist(depth):
                        r.stop()
        
except Exception as e:
        print(e)
        #rospy.loginto("node now terminated")
