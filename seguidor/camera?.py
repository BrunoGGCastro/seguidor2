from __future__ import print_function
import numpy as np
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
yellowLower =(45,23,56)
yellowUpper = (64, 255, 255)

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("agent/camera/color/image_raw",Image,queue_size=10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("agent/camera/color/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)
    #hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    ret, thresh_basic = cv2.threshold(cv_image,65,255,cv2.THRESH_BINARY_INV)

    #cv2.imshow("mask image", mask)
    cv2.imshow("Basic Binary Image",thresh_basic)
    cv2.imshow("Image window",cv_image)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)




