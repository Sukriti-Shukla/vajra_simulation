 #!/usr/bin/env python2.7
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
from visualization_msgs.msg import Marker
from sensor_msgs.msg import PointCloud 
print ("Hello!")
rospy.init_node('pothole', anonymous=True)
rospy.loginfo("Hello ROS!")
bridge = CvBridge()
img_pub1 = rospy.Publisher('/pothole', Image, queue_size=10)
# Define a function to show the image in an OpenCV Window
def show_image(img):
    cv2.imshow("Image Window", img)
    cv2.waitKey(3)

# Define a callback for the Image message
def image_callback(img_msg):
     # log some info about the image topic
        rospy.loginfo(img_msg.header)
 # Try to convert the ROS Image message to a CV2 Image
        try:
          cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
        except CvBridgeError:
          rospy.logerr("CvBridge Error: {0}".format(e))

        cv_image = cv2.transpose(cv_image)
        imgray = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
        contours =  cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
        cv2.drawContours(cv_image, contours, -1, (0,255,0), 3)
        img_pub1.publish(bridge.cv2_to_imgmsg(cv_image, encoding="passthrough"))
      # Show the converted image
        show_image(cv_image)
 # Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
sub_image = rospy.Subscriber("/camera/right/image_raw", Image, image_callback)

# Initialize an OpenCV Window named "Image Window"
cv2.namedWindow("Image Window", 1)

 # Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
while not rospy.is_shutdown():
     rospy.spin()