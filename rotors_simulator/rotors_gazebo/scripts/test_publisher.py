#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Bool

if __name__ == '__main__':
  rospy.init_node('talker', anonymous=True)

  pub = rospy.Publisher('chatter', Bool, queue_size=10)
  print("x\nx\nx\nstarting wait\nx\nx\nx\n")
  d = rospy.Duration(5, 0)
  rospy.sleep(d)
  print("x\nx\nx\nx\nx 5 sec sleep done \nx\nx\nx\n")
  
  hello_str = True
  rospy.loginfo(hello_str)
  pub.publish(hello_str)
##################################################################print 10
  print("x\nx\nx\nstarting wait anew\nx\nx\nx\n")
  d = rospy.Duration(10, 0)
  rospy.sleep(d)
  print("x\nx\nx\nx\nx 10 sec sleep done \nx\nx\nx\n")
  hello_str = False
  rospy.loginfo(hello_str)
  pub.publish(hello_str)

###############################################3######## 8 sec
  # print("x\nx\nx\nstarting wait trinew\nx\nx\nx\n")
  # d = rospy.Duration(8, 0)
  # rospy.sleep(d)
  # print("x\nx\nx\nx\nx 10 sec sleep done \nx\nx\nx\n")
  hello_str = True
  rospy.loginfo(hello_str)
  pub.publish(hello_str)

  hello_str = False
  rospy.loginfo(hello_str)
  pub.publish(hello_str)  
  hello_str = True
  rospy.loginfo(hello_str)
  pub.publish(hello_str)

  hello_str = False
  rospy.loginfo(hello_str)
  pub.publish(hello_str)  
  hello_str = True
  rospy.loginfo(hello_str)
  pub.publish(hello_str)

  hello_str = False
  rospy.loginfo(hello_str)
  pub.publish(hello_str)  

  rospy.spin()




