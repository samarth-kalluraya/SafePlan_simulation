
#include "ros/ros.h"
#include "std_msgs/Bool.h"
bool is_path_ready = false;
void chatterCallback(const std_msgs::Bool::ConstPtr& msg)
{
  //ROS_INFO("I heard: [%s]", msg->data.c_str());
  is_path_ready = msg->data;
  std::cout<<"\n         in callback : ";
  std::cout<<is_path_ready;
}


int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);

  std::cout<<"\n         before waitxxxxxxxxxxxxxxxx : ";
  while (!is_path_ready && ros::ok()) {
    std::cout<<"\nwaiting for path : ";
    std::cout<<is_path_ready;
    ros::spinOnce();
    ros::Duration(0.5).sleep();
  }
  std::cout<<"\n         Out of wait!!!!!!!!!!!!!!!! : ";
  std::cout<<"\n finally path : ";
  std::cout<<is_path_ready;
  int a = 5;
  int b = 7;
  int c = a+b;
  std::cout<<"\nc : ";
  std::cout<<c;
  

  for (int i=0; i<5; i++){
    std::cout<<"\nthis is i: ";
    std::cout<<i;
  }


  std::cout<<"\nlast line ";
  b = 7;
  for (int i = 0; i < 100; ++i) {
        
        // ros::Subscriber path_sub = nh.subscribe("path_ready", 10, chatterCallback);
        while (!is_path_ready && ros::ok()) {
          std::cout<<"\nwaiting for path : ";
          std::cout<<is_path_ready;
          ros::spinOnce();
          ros::Duration(0.5).sleep();
          // i=0;
        }
        double t = 1;
        std::cout<<"\npath_ready "<<i<<": "<<is_path_ready<<"\n";

        ros::Duration(t).sleep();
        ros::spinOnce();

  }
  ros::spin();
  //return 0;
}
// %EndTag(FULLTEXT)%
